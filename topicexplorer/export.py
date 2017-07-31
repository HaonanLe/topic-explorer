from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import input
from builtins import range

from configparser import RawConfigParser as ConfigParser
import os.path
from zipfile import ZipFile

from topicexplorer.lib.util import is_valid_configfile

def build_manifest(config_file, corpus_file, model_pattern, topic_range,
                   cluster_path=None):
    files = [config_file, corpus_file]

    for k in topic_range:
        files.append(model_pattern.format(k))

    if cluster_path:
        files.append(cluster_path)
    return files


def zip_files(outfile, manifest, verbose=True):
    root = os.path.commonpath(map(os.path.abspath, manifest))
    files = [(f, os.path.relpath(f, root)) for f in manifest]

    with ZipFile(outfile, 'w') as output:
        print("Constructing archive {}".format(outfile))
        for path, arcpath in files:
            if verbose:
                print("Exporting {}".format(arcpath))
            output.write(path, arcpath)


def populate_parser(parser):
    parser.add_argument('config', type=lambda x: is_valid_configfile(parser, x),
                        help="Configuration file path")
    parser.add_argument('-o', '--output', help="Output path for arcive (.tez)",
                        required=False, default=None)
    return parser


def main(args=None):
    # load in the configuration file
    config = ConfigParser({
        'certfile': None,
        'keyfile': None,
        'ca_certs': None,
        'ssl': False,
        'port': '8000',
        'host': '0.0.0.0',
        'icons': 'link',
        'corpus_link': None,
        'doc_title_format': '{0}',
        'doc_url_format': '',
        'raw_corpus': None,
        'label_module': None,
        'fulltext': 'false',
        'topics': None,
        'cluster': None,
        'corpus_desc' : None,
        'home_link' : '/',
        'lang': None})
    #open config for reading
    with open(args.config, encoding='utf8') as configfile:
        config.read_file(configfile)

    # clean up output file path
    if args.output is None:
        args.output = args.config.replace('.ini', '.tez') 
    if not args.output.endswith('.tez'):
        args.output += '.tez'

    # path variables
    context_type = config.get('main', 'context_type')
    corpus_file = config.get('main', 'corpus_file')
    model_pattern = config.get('main', 'model_pattern')
    cluster_path = config.get('main', 'cluster')
    
    # topic variables
    if config.get('main', 'topics'):
        topic_range = eval(config.get('main', 'topics'))

    # get manifest for zip file
    filenames = build_manifest(
        args.config, corpus_file, model_pattern, topic_range, cluster_path)

    zip_files(args.output, filenames)


if __name__ == '__main__':
    main()
