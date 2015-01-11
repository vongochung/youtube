__author__ = 'Jean-Bernard Ratte - jean.bernard.ratte@unary.ca'

from os import listdir, path
from subprocess import call, check_output, CalledProcessError


SOURCE_FOLDER = "Video files folder location: "
BATCH_MERGE = "Merge all video in subfolders (Y/N)? "
VALIDATION = ' - The output file is named "%s"'
MERGE_THIS = ' - Do you want to merge "%s" (Y/N)? '
ERROR_FILE_COUNT = 'Could not merge, there is not enough files in folder %s'


def is_choice(val):
    if val.upper() in ['Y', 'N']:
        return True


def ask(msg, keep_asking=None):
    resp = str(raw_input(msg))

    if is_choice(resp):
        if resp.upper() == "Y":
            return True

        else:
            return False

    print 'Invalid answer'
    if keep_asking:
        ask(msg, keep_asking=keep_asking)


def ask_source(msg, keep_asking=None):
    resp = str(raw_input(msg))

    if path.exists(resp):
        return resp

    print 'Invalid path'
    if keep_asking:
        ask_source(msg, keep_asking=keep_asking)


def append_dir(dirname, filename):
    return ''.join([dirname.replace(' ', '\ '), '/', filename.replace(' ', '\ ')])


def build_cmd(dir, output, *files):
    files = map(lambda file: append_dir(dir, file), list(files))
    return ' '.join(["mp4box -force-cat", '-add', files.pop(0), ''.join(['-cat ' + i for i in files]),
                     append_dir(dir, output)])


if __name__ == '__main__':
    print '\r\n---------------------------------'
    print '-     This tool uses MP4Box     -'
    print '-  http://gpac.sourceforge.net  -'
    print '---------------------------------'

    created_files = []
    try:
        check_output('mp4box -version', shell=True)

        source = ask_source(SOURCE_FOLDER, keep_asking=True)
        # Merge all file in source directory without asking for confirmation
        is_batch = ask(BATCH_MERGE, keep_asking=True)

        folders = [folder for folder in listdir(source) if not folder[0] == '.']
        for directory in folders:
            absolute_directory = source + '/' + directory

            # Files to merge
            files = [f for f in listdir(absolute_directory) if not f[0] == "." and f.find('.mp4') > -1]

            # Merged file name
            merge_name = ''.join([directory[directory.rfind("/") + 1:], '.mp4'])

            merge = True
            if not is_batch:
                merge = ask(MERGE_THIS % merge_name, keep_asking=True)

            if merge:
                if len(files) > 1:
                    print VALIDATION % merge_name
                    cmd = build_cmd(absolute_directory, merge_name, *files)
                    print call(cmd, shell=True)

                    # Hold a reference to the newly created MP4 file
                    created_files.append(append_dir(absolute_directory, merge_name))

                else:
                    print ERROR_FILE_COUNT % directory[directory.rfind("/") + 1:]

        print "Done!"

    except CalledProcessError:
        print 'Unable to check MP4Box version, you should check your MP4Box installation'
        print 'Compile from source, see http://gpac.sourceforge.net/'

    except (KeyboardInterrupt, SystemExit):
        print '\r\nDeleting newly created files'

        for file in created_files:
            return_code = call(['rm', file])

        print 'Bye.'