#!/usr/bin/env python3


from ffcuesplit import version
from ffcuesplit.main import parse_args, show_error, start_the_process


start_the_process(parse_args(version))
#try:
#    start_the_process(parse_args(version))
#except Exception as e:
#    show_error(e)
