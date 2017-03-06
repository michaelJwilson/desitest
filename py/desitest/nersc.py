"""
Tools for updating and testing code at NERSC
"""

from __future__ import absolute_import, division, print_function
import sys, os
import subprocess
import time

def update(basedir=None, logdir='.'):
    '''TODO: Document'''
    if not os.path.exists(basedir):
        raise ValueError("Missing directory {}".format(basedir))

    logdir = os.path.abspath(logdir)
    if not os.path.exists(logdir):
        raise ValueError("Missing log directory {}".format(logdir))

    results = dict()

    #- repositories to update in order of dependencies
    #- TODO: consider speclite, specsim, and redmonster or redrock
    repos = [
        'desiutil',
        'specter',
        'desimodel',
        'desitarget',
        'desispec',
        'desisim',
    ]

    for repo in repos:
        repo_results = dict()
        repodir = os.path.join(basedir, repo, 'master')
        if not os.path.exists(repodir):
            repo_results['status'] = 'FAILURE'
            repo_results['log'] = 'Missing directory {}'.format(repodir)
        else:
            os.chdir(repodir)
            repo_results['log'] = ['--- {}'.format(repodir), '']
            commands = ["git pull", "python setup.py test"]
            
            #- special case for desimodel: also update svn data
            if repo == 'desimodel':
                commands = ['svn update data/',] + commands

            for cmd in commands:
                x = subprocess.run(cmd.split(), stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, universal_newlines=True)
                repo_results['log'].extend( ['--- '+cmd, x.stdout] )
                if x.returncode != 0:
                    repo_results['status'] = 'FAIL'
                    break
                else:
                    repo_results['status'] = 'ok'            

        repo_results['log'] = '\n'.join(repo_results['log'])
        results[repo] = repo_results
        ### print('{:20s}  {}'.format(repo, results[repo]['status']))

    for repo in repos:
        logfile = os.path.join(logdir, repo+'.log')
        with open(logfile, 'w') as fx:
            fx.write(results[repo]['log'])

    #- Write index.html in log directory
    with open(os.path.join(logdir, 'index.html'), 'w') as fx:
        fx.write('<html>\n<body>\n')
        fx.write('<h1>Updated {}</h1>\n'.format(time.asctime()))
        fx.write('<table>\n')
        for repo in repos:
            fx.write('  <tr>\n')
            fx.write('    <td>{}</td>\n'.format(repo))
            fx.write('    <td><a href="{}.log">{}</a></td>\n'.format(repo, results[repo]['status']))
            fx.write('  </tr>\n')
        fx.write('</table>\n</body>\n</html>\n')            

    return results
