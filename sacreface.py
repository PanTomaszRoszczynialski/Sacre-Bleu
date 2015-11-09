""" All facebook related methods are in this file """

import settings as s
import facebook

# Secrets are used for facebook api authentication
def get_secrets(filenames):
	with open(filenames[0], 'r') as myfile:
		token = myfile.read().replace('\n','')

	with open(filenames[1], 'r') as idfile:
            page_id = idfile.read().replace('\n','')

	return token, page_id

# Config object is used in python facebook module
def make_cfg():
    token, pageid = get_secrets(['token.secret', 'pageid.secret'])
    cfg = {
            'page_id' : '119890141687062',
            'access_token' : token
            }

    return cfg

# Get python access to facebook api 
def get_api():
    cfg = make_cfg()
    graph = facebook.GraphAPI(cfg['access_token'], version='2.4')
    #  Get page token to post as the page. You can skip
    #  the following if you want to post as yourself.
    resp = graph.get_object('me/accounts')
    page_access_token = None
    for page in resp['data']:
	if page['id'] == cfg['page_id']:
            page_access_token = page['access_token']
            graph = facebook.GraphAPI(page_access_token, version='2.4')
    return graph
# You can also skip the above if you get a page token:
#http://stackoverflow.com/questions/8231877/facebook-access-token-for-pages
# and make that long-lived token as in Step 3

# Get an ID of a facebook album for a given date
# or create it if it doesnt exist
def get_album_id(api, foldername):
    # foldername must be named with current date
    # following the YMD_FORMAT defined in settings
    date = foldername

    # Name album with the current pic date
    time_struct = time.strptime(date, s.YMD_FORMAT)
    album_name = time.strftime('%Y %B %d', time_struct)

    albums = api.get_object('me/albums')['data']

    # Iterate through albums untill the proper one is found
    # TODO some better search mechanism might be desired
    id = None
    for bum in albums:
	#print bum['name']
	if album_name in bum['name']:
            id = bum['id']

    # Create album is nothing were found
    if id is None:
	resp = api.put_object(parent_object = 'me',\
                              connection_name = 'albums',\
                              message = 'Album',\
                              name = album_name)
	id = resp['id']

    return id

# Provide full path to the picture you want to upload
def post_to_wall(picpath, message):
    # Get facebook api
    api = get_api()

    # Pictures posted to wall are held at the main dir
    # FIXME - add some dir structure
    api.put_photo(image = open(picpath),\
                  message = message)

# TODO - refactor this a lot
def post_to_album(picInfo, message):
    # Get facebook api
    api = get_api()

    # Date names directories
    picname = picInfo[0]
    picpath = picInfo[1]
    datestr = picname[0:10]

    # Get desired album id
    id = get_album_id(api, picname)

    # Add clock information to post message
    cock = picname[12:18]
    struct = time.strptime(cock, '%H%M%S')
    clock_msg = time.strftime('%X', struct)

    # Extend message with clock info
    message = message + '\n\n\n' + clock_msg

    # and ip
#    ipinfo = subprocess.check_output('ifconfig |grep inet', shell=True)
 #   message = message + '\n\n\n' + ipinfo
    api.put_photo(image = open(picpath),\
		  message = message,\
		  album_path = id + '/photos')
