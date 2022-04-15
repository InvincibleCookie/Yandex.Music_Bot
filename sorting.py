from yandex_music import Client
import time


def autorisation(link):
    token = link[link.find('token=') + 6:link.find('&token_type')]
    client = Client(token).init()
    return client


def get_playlist(name, client):
    p_list = client.users_playlists_list()
    p_kind = 0
    p_uid = 0
    Name = name[0:]
    for e in p_list:
        if e["title"] == Name:
            p_kind = e['kind']
            p_uid = e['uid']
    return client.users_playlists(p_kind, p_uid)


def sorting(playlist, sorting_by, client):
    if sorting_by == 'По исполнителю и альбому':
        playlist.tracks.sort(key=lambda x: (x['track']['artists'][0]['name'], x['track']['albums'][0]['id'],
                                            x['track']['albums'][0]['track_position']['volume'],
                                            x['track']['albums'][0]['track_position']['index']),
                             reverse=True)
    elif sorting_by == 'По исполнителю':
        playlist.tracks.sort(key=lambda x: (x['track']['artists'][0]['name'], x['track']['title']), reverse=True)


    elif sorting_by == 'По альбому':
        playlist.tracks.sort(
            key=lambda x: (x['track']['albums'][0]['title'], x['track']['albums'][0]['track_position']['volume'],
                           x['track']['albums'][0]['track_position']['index']), reverse=True)

    client.users_playlists_delete_track(playlist.kind, 0, len(playlist.tracks), playlist.revision)
    playlist.revision += 1
    return playlist.tracks.copy()


def finish_sorting(playlist_tracks, playlist):
    for e in playlist_tracks:
        playlist.insert_track(e['id'], e['track']['albums'][0]['id'])
        playlist.revision += 1


def liked_songs(client):
    try:
        playlist = get_playlist('Мне нравится', client)
    except:
        client.users_playlists_create('Мне нравится')
        playlist = get_playlist('Мне нравится', client)

    if len(playlist.tracks) > 0:
        client.users_playlists_delete_track(playlist.kind, 0, len(playlist.tracks), playlist.revision)
        playlist.revision += 1
    time.sleep(20)
    if len(client.users_likes_tracks()) > 200 and len(client.users_likes_tracks()) < 500:
        for e in client.users_likes_tracks()[::-1][0: len(client.users_likes_tracks()) // 3]:
            playlist.insert_track(e['id'], e['album_id'])
            playlist.revision += 1
        time.sleep(20)

        for e in client.users_likes_tracks()[::-1][
                 len(client.users_likes_tracks()) // 3: 2 * len(client.users_likes_tracks()) // 3]:
            playlist.insert_track(e['id'], e['album_id'])
            playlist.revision += 1
        time.sleep(20)

        for e in client.users_likes_tracks()[::-1][
                 2 * len(client.users_likes_tracks()) // 3: len(client.users_likes_tracks())]:
            playlist.insert_track(e['id'], e['album_id'])
            playlist.revision += 1

    elif len(client.users_likes_tracks()) >= 500:

        for e in client.users_likes_tracks()[::-1][0: len(client.users_likes_tracks()) // 5]:
            playlist.insert_track(e['id'], e['album_id'])
            playlist.revision += 1
        time.sleep(20)

        for e in client.users_likes_tracks()[::-1][
                 len(client.users_likes_tracks()) // 5: 2 * len(client.users_likes_tracks()) // 5]:
            playlist.insert_track(e['id'], e['album_id'])
            playlist.revision += 1
        time.sleep(20)

        for e in client.users_likes_tracks()[::-1][
                 2 * len(client.users_likes_tracks()) // 5: 3 * len(client.users_likes_tracks()) // 5]:
            playlist.insert_track(e['id'], e['album_id'])
            playlist.revision += 1

        for e in client.users_likes_tracks()[::-1][
                 3 * len(client.users_likes_tracks()) // 5: 4 * len(client.users_likes_tracks()) // 5]:
            playlist.insert_track(e['id'], e['album_id'])
            playlist.revision += 1
        time.sleep(20)

        for e in client.users_likes_tracks()[::-1][
                 4 * len(client.users_likes_tracks()) // 5: len(client.users_likes_tracks())]:
            playlist.insert_track(e['id'], e['album_id'])
            playlist.revision += 1
    else:
        for e in client.users_likes_tracks()[::-1]:
            playlist.insert_track(e['id'], e['album_id'])
            playlist.revision += 1


def playlist_copy(name, client):
    client.users_playlists_create(f'{name}.копия')
    playlist = get_playlist(name, client)
    copy_playlist = get_playlist(f'{name}.копия', client)
    return playlist, copy_playlist


def final_copy(songs_reversed, copy_playlist):
    for e in songs_reversed:
        copy_playlist.insert_track(e['id'], e['track']['albums'][0]['id'])
        copy_playlist.revision += 1
