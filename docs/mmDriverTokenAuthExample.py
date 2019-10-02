
# A simple example to retrieve all users for a team while using a _token_ 
# from the .netrc file instead of a password (as requests assumes by default)

import logging 
import requests
import netrc

from mattermostdriver import Driver

logging.basicConfig( format='%(levelname)s - %(name)s - %(asctime)s - %(message)s' )
logger = logging.getLogger( 'MattermostManager' )
logger.setLevel( logging.INFO )

# requests overrides the simple authentication token header if it finds the entry in 
# the ~/.netrc file. Since we want to use ~/.netrc to retrieve the _token_, we need
# to provide our own Authenticator class:

class TokenAuth( requests.auth.AuthBase ) :
    def __call__( self, r ) :
        # Implement my authentication
        mmHost = 'mattermost.host.in.netrc'
        (login, account, password) = netrc.netrc().authenticators( mmHost )
        r.headers[ 'Authorization' ] = "Bearer %s" % password
        return r


class MattermostManager( object ) :

    def __init__( self ) :

        # Get the _token_ (as "password") from the ~/.netrc file.
        # the corresponding line in the file should look like:
        # <mattermost.host.in.netrc> foo foo <long-string-of-token>
        # The "login" and "account" (both set to "foo" in the example are ignored)
        
        mmHost = 'mattermost.host.in.netrc'
        (login, account, password) = netrc.netrc().authenticators( mmHost )
        logger.debug( "Going to set up driver for connection to %s " % (mmHost,) )

        self.mmDriver = Driver( options={
            'url'    : mmHost,
            'scheme' : 'https',
            'port'   : 443,
            'auth'   : TokenAuth, # use the new Authenticator class defined above
        } )

        self.mmDriver.users.get_user( user_id='me' )

    def getTeamMembers( self, teamName ) :

        # for restricted teams, we need to get the ID first, and
        # for this, we need to have the "name" (as in the URL), not
        # the "display name", as shown in the GUIs:

        team0 = self.mmDriver.teams.get_team_by_name( teamName )
        logger.debug( 'team by name %s : %s' % (teamName, team0) )
        teamId = team0[ 'id' ]

        team = self.mmDriver.teams.check_team_exists( teamName )
        logger.debug( 'team %s - exists: %s' % (teamName, team[ 'exists' ]) )
        if not team[ 'exists' ] :
            logger.error( 'no team with name %s found' % teamName )
            return

        logger.debug( 'found team %s: %s' % (teamName, self.mmDriver.teams.get_team( teamId )) )

        users = self._getAllUsersForTeam( teamId )
        logger.debug( 'found %s users for team "%s"' % (len( users ), teamName) )

        return users

    def _getAllUsersForTeam( self, teamId ) :

        # get all users for a team
        # with the max of 200 per page, we need to iterate a bit over the pages

        users = [ ]
        pgNo = 0
        teamUsers = self.mmDriver.users.get_users( params={ 'in_team'  : teamId,
                                                            'page'     : str( pgNo ),
                                                            'per_page' : 200,
                                                            } )
        while teamUsers :
            users += teamUsers
            pgNo += 1
            teamUsers = self.mmDriver.users.get_users( params={ 'in_team'  : teamId,
                                                                'per_page' : 200,
                                                                'page'     : str( pgNo ),
                                                                } )
        return users

if __name__ == '__main__' :
    mmM = MattermostManager()
    mmM.getTeamMembers( 'myTeam' )
