import sys, os
from Parser import Parser

INPUT_SPECIFIER = "\input"

def specify_filename(argument_path):
    filename = input("Plase specify the name of the file which includes "
                     "all files to parse (no extension needed)\n")
    if ".tex" not in filename:
        filename = filename + ".tex"
    return os.path.join(argument_path, filename)

def choose_output_name():
    """
    the user can decided upon the name of the output file
    :return: the name of the file with extenstion = tex
    """
    filename = input("Please insert a filename for your output file "
                     "(no extension needed)\n")
    if ".tex" not in filename:
        return filename + ".tex"
    return filename

def parse_file(input_file, parser, argument_path):
    """
    uses the parser object and parses a single file from the supplied directory
    :param input_file: the input file to parse
    :param output_file: the output file
    :param parser: parser object
    :return: None
    """
    parser.parse_main_file(input_file, argument_path)
    input_file.close()

if __name__ == "__main__":
    """
    parses the input path and calls parse_file on each input file.
    """
    if not len(sys.argv) == 2:  # invalid args
        sys.exit("USAGE: please provide a valid input path")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path): # the filepath is a directory
        all_files_in_directory = [os.path.join(argument_path, filename) for
                                  filename in os.listdir(argument_path)]
    else: # the filepath is a single file, not supported
        sys.exit("Please provide a path to the directory where all files are,"
                 " and not a path of a single file\n")
    file_to_parse = specify_filename(argument_path)
    output_path = choose_output_name()
    with open(output_path, 'w') as output_file:
        parser = Parser(output_file, all_files_in_directory)
        with open(file_to_parse, 'r') as input_file:
            parse_file(input_file, parser, argument_path)
        parser.add_all_images() # add images after all input files
    output_file.close()