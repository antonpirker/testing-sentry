# The gunicorn "configuration" file

import cProfile

profile = cProfile.Profile()

def pre_request(worker, req):
    print("enabling profile for the request")
    profile.enable()

def post_request(worker, req, *args):
    profile.disable()
    print("request done, profile disabled now")

def worker_exit(server, worker):
    # Write pstats to file that can then by viewed with snakeviz
    # profile.dump_stats("latest.pstats")

    # Print stats to console
    profile.print_stats()

    print("process exiting, dumping stats to file")
