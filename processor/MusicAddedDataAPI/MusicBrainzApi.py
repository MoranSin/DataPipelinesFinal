import musicbrainzngs as mbz 

def get_gender(artist_name):
    mbz.set_useragent('TheRecordIndustry.io', '0.1')
    artist_list = mbz.search_artists(query=artist_name)['artist-list'] 
    name = artist_list[0] 
    return(name["gender"])