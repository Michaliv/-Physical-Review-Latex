import os, sys
class Parser:
    """
    class Parser parses a given set of files into one output file, where all
    images appear in the end of the output file- by the same order they
    appeared in in the original input files
    """

    # possible image identifiers:
    IMAGE_IDENTIFIERS = {"\\begin{figure}":"\\end{figure}",
                         "\\begin{figure*}":"\\end{figure*}",
                         "\\begin{wrapfigure}": "\\end{wrapfigure}"}

    INPUT_SPECIFIER = "\input"

    INSIDE_IMAGE = False

    IMAGES_PART = []

    def __init__(self, output_file, all_files_in_directory):
        """
        ctor of Parser class recives a list of all files in the given directory
        and the output file which will eventually contain the content of all
        files specified in the input file
        :param output_file: the output file of the program
        :param all_files_in_directory: a list of all files in the directory,
        with their paths
        """
        self.all_files_in_directory = all_files_in_directory
        self.output_file = output_file

    def parse_main_file(self, input_file, argument_path):
        """
        writes to the output file only until we encounter the list of files
        specified by "\input", then- "spills" into the output file the content
        of the file which is inside the brackets {}. continues to do so until
        we reach the end of the input file.
        :param input_file: the main file, where the list of all files is
        :param argument_path: the path of the directory where all files are in
        :return: None
        """
        for line in input_file:
            if Parser.INPUT_SPECIFIER in line:
                filename =self.find_file_to_translate(line, argument_path)
                if filename in self.all_files_in_directory:
                    with open(filename, 'r') as single_file:
                        self.parse_single_file(single_file)
                        self.output_file.write("\n \n")
                        single_file.close()
                        continue
            self.output_file.write(line)

    def find_file_to_translate(self, line, argument_path):
        """
        is given the line which starts with "\input", and returns the name of
        the file needed to be parsed
        :param line: the line which contains the name of the file
        :param argument_path: the path of the directory where all files are in
        :return: the name and path of the file to be parsed
        """
        index_of_starter_of_filename = line.rfind("{") # find beginning of name
        index_of_end_of_filename = line.rfind("}") # find the end
        cropped_line = line[index_of_starter_of_filename + 1:index_of_end_of_filename]
        file_path = os.path.join(argument_path, cropped_line)
        return file_path

    def parse_single_file(self, input_file):
        """
        parses a single file. if we are in an image section, calls helper functions
        that will later help add images in the end of the output file.
        in any other case, writes the line from the original file to the output file
        :param input_file: the current input file
        :return: None
        """
        for line in input_file:
            for identifier in Parser.IMAGE_IDENTIFIERS.keys():
                if identifier in line:
                    Parser.INSIDE_IMAGE = True
            if Parser.INSIDE_IMAGE: # while inside image section, don't write to output
                self.add_to_images_part(line)
            else:
                self.output_file.write(line)

    def add_to_images_part(self, line):
        """
        in case we entered a section in the text which represents an image,
        add all the lines in this part to a global class array IMAGES_PART,
        until we reach the end of the image section.
        :param line: the current line inside the image section
        :return: None
        """
        Parser.IMAGES_PART.append(line)
        for end_identifier in Parser.IMAGE_IDENTIFIERS.values():
            if end_identifier in line:
                Parser.INSIDE_IMAGE = False
                Parser.IMAGES_PART.append("\n")

    def add_all_images(self):
        """
        this function is called after we finish parsing all the input files,
        and writes to the output file all the text from the image sections
        :return:
        """
        for image in Parser.IMAGES_PART:
            self.output_file.write(image)