"""Wraps an individual scheme/siod command to festival"""

import cmd

"""
festival_client.py - a python socket client for festival_server

Copyright (C) 2014
Thomas J. Webb (thomas@thomaswebb.net) 8/2014
Music Mastermind, Inc.
All rights reserved.

The authors hereby grant permission to use, copy, modify, distribute,
and license this software and its documentation for any purpose, provided
that existing copyright notices are retained in all copies and that this
notice is included verbatim in any distributions. No written agreement,
license, or royalty fee is required for any of the authorized uses.
Modifications to this software may be copyrighted by their authors
and need not follow the licensing terms described here, provided that
the new terms are clearly indicated on the first page of each file where
they apply.

IN NO EVENT SHALL THE AUTHORS OR DISTRIBUTORS BE LIABLE TO ANY PARTY
FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES
ARISING OUT OF THE USE OF THIS SOFTWARE, ITS DOCUMENTATION, OR ANY
DERIVATIVES THEREOF, EVEN IF THE AUTHORS HAVE BEEN ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

THE AUTHORS AND DISTRIBUTORS SPECIFICALLY DISCLAIM ANY WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.  THIS SOFTWARE
IS PROVIDED ON AN "AS IS" BASIS, AND THE AUTHORS AND DISTRIBUTORS HAVE
NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
MODIFICATIONS.
"""

class FestivalCommand(cmd.Cmd, object):
    """Command interpreter for python festival-client"""

    def __init__(self, festival_client):
        super(FestivalCommand, self).__init__()

        self.prompt = "festival> "
        self.festival_client = festival_client

    def do_EOF(self, line):
        print("")
        return True

    def do_quit(self, line):
        return True

    def do_exit(self, line):
        return self.do_quit(line)

    def emptyline(self):
        pass

    def default(self, line):
        # Ignoring audio responses for now
        scheme_responses, audio_responses = self.festival_client.send_message(line)
        for scheme_response in scheme_responses:
            print(scheme_response)
