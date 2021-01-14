from zhanglyLabTools import script_generator
from pathlib import Path
import argparse
import json
import os

def main():
    # setting up parsers
    parser = argparse.ArgumentParser('zhanglyLabTools')
    with open(os.path.join(Path.home(), '.zhanglyLabToolsRC.json'), 'r') as f:
        settings = json.load(f)

    subcommandParsers = parser.add_subparsers(title="zhanglyLabTools",
                                            dest="subcommand", )

    script_generators_settings = settings['script_generators']
    template_sub_dict = settings['templates']
    generator_parsers = dict()
    generators = dict()

    for generator_name, generator_settings in script_generators_settings.items():
        sub_parser = subcommandParsers.add_parser(generator_name)
        generator_parsers[generator_name] = sub_parser

        generator = script_generator(generator_name, generator_settings, template_sub_dict)
        generators[generator_name] = generator

        generator.set_argparser(sub_parser)

        sub_parser.add_argument('--opath', '-O', 
                                dest='opath', 
                                help='PBS output path', 
                                default='.')
        
        sub_parser.add_argument('--template',
                                dest='template', 
                                help='template path', 
                                default=False)

    args = parser.parse_args()
    generator = generators[args.subcommand]

    if args.template:
        with open(args.template, 'r') as f:
            template_content = f.read()
        generator.load_template(template_content)

    # expansion mode
    if args.job_name.__str__()[-5:] == '.list':
        with open(args.job_name, 'r') as f:
            job_names = [s.replace('\n', '') for s in f.readlines()]
        
        num_jobs = len(job_names)
        arg_list_dict = {'job_name': job_names}

        for job_name in job_names:
            for key, value in args.__dict__.items():
                if value.__str__()[-5:] == '.list':
                    with open(value, 'r') as f:
                        arg_list_dict[key] = [s.replace('\n', '') for s in f.readlines()]
                else:
                    arg_list_dict[key] = [value] * num_jobs

        for i in range(num_jobs):
            arg_dict = {key: value[i] for key,value in arg_list_dict.items()}

            with open(os.path.join(args.opath, arg_dict['job_name'] + '.pbs'), 'w') as f:
                f.write(generator.render(arg_dict))
    else:
        with open(os.path.join(args.opath, args.job_name + '.pbs'), 'w') as f:
            f.write(generator.render(args.__dict__))

