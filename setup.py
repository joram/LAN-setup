import fileinput
import os
import time 

debug = True
############################
#  CSCU LAN SETUP
#	these scripts are to automatically setup lan parties
#	author:raznatal
############################
print "LAN SETUP:" 


############################
#  REQUIRED ACTIVITES 
############################
desktop = os.environ['USERPROFILE']+ "\\Desktop"

# make games directory
gamesdir = desktop+"\\games"
if not os.path.isdir(gamesdir):
    os.mkdir(gamesdir)
if debug == True:
	print "games directory:"+gamesdir

# make utorrent directory
utorrentdir = gamesdir+"\\utorrent"
if not os.path.isdir(utorrentdir):
    os.mkdir(utorrentdir)
print "utorrent directory:"+utorrentdir

# copy over utorrent and config files
os.system ("xcopy /FY /s %s %s" % ('utorrent', utorrentdir))
utorrent = utorrentdir+"\\utorrent.exe"


############################
#  WALK THROUGH ALL GAMES
#  - to add a game
#	create a torrent, and put it in the torrents folder
#	the name of the torrent MUST be the same as the first parameter of the game
#	add any registry edits as the second parameter as a list, if there is none, add an empty list
#  - to remove a game
#	comment out the game from the list of games
#	please don't delete the game from the list, so we can add it back in easily later
############################

#defining a "game" object
#   name
#	the name of the game, the folder it will reside in, and the torrent file
#   exe file
#	the exe file in relation to the base directory of the game
#   regedits
#	a list of all registry edits that need to be made for this game
#   linkparams (index, iconFile)
#	an array containing:
#	   - the index within the icon file, for which file to use
#	   - the location of the icon file from the base of the game dir
class game:
	def __init__(self, name, exe, regedits=[], linkparams=[]):
		self.name = name
		self.torrent = name+".torrent"
		self.regedits = regedits
		self.linkParameters = linkparams
		self.exe = exe

# list all games
games = [
	game("Armagetron", "a.exe", regedits = ["a", "b"]),
	game("Counter Strike", "hl.exe", linkparams = [1,"hl.exe"] ),
	game("teamFortress 2", "hl.exe" )
]

# loop through games
for g in games:
	print "\t"+g.name

	#open torrent
	utorrent_switches = ["/NOINSTALL ", "/HIDE ", "/DIRECTORY "]

	#build shortcut command
	link 	= desktop+"\\"+g.name+".lnk"
	exe 	= gamesdir+"\\"+g.name+"\\"+g.exe
	base	= gamesdir+"\\"+g.name
	if len(g.linkParameters) == 2:
		index= g.linkParameters[0] # icon index
		icon = g.linkParameters[1] # icon location
	else:
		index= 0
		icon = ""
	cmd = 'makeLink.exe /q "%s" "%s" "" "%s" "" %s "%s"' % (link, exe, base, index, icon)	
	if debug == True:
		print "\t  created shortcut"

	# create shortcut
	os.system(cmd);

	#do regedits
	for regedit in g.regedits:
		if debug == True:
			print "\t  regedit:"+regedit

	# open torrent
	dir = gamesdir+"\\"+g.name
	torrent = os.getcwd()+"\\torrents\\"+g.torrent
	if os.path.isfile(torrent):
		os.system('%s /noinstall /directory %s "%s"' % (utorrent, dir, torrent))
		print "\t  opened torrent"
	else:
		print "\t  !!! no torrent found !!! "+torrent



time.sleep(3)