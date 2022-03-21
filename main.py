import sqlalchemy

from pprint import pprint

engine = sqlalchemy.create_engine('postgresql://postgres:Abkbgg090915@localhost:5432/postgres')
pprint(engine)

connection = engine.connect()
# print(connection)
# pprint(engine.table_names())


#1.количество исполнителей в каждом жанре;
select_1 = connection.execute('''
SELECT genre_id, COUNT(executor_id) FROM executor_genre
GROUP BY genre_id 
ORDER BY COUNT(executor_id) DESC
''').fetchall()
pprint(f'Количество исполнителей в каждом жанре: {select_1}')

#2.количество треков, вошедших в альбомы 2019-2020 годов
select_2 = connection.execute('''
SELECT COUNT(track.title) FROM track
JOIN album ON track.album = album_id
WHERE year_of_recording BETWEEN '2019' AND '2020'
''').fetchall()
pprint(f'Количество треков, вошедших в альбомы 2019-2020 годов: {select_2}')

#3.средняя продолжительность треков по каждому альбому
select_3 = connection.execute('''
SELECT album.title, SUM(track.duration) FROM track
JOIN album ON track.album = album_id
GROUP BY album.title
ORDER BY SUM(track.duration) DESC
''').fetchall()
pprint(f'Cредняя продолжительность треков по каждому альбому: {select_3}')

#4.все исполнители, которые не выпустили альбомы в 2020 году
select_4 = connection.execute('''
SELECT e.name FROM executor_album  ea
JOIN executor e ON ea.executor_id = e.executor_id
JOIN album a ON ea.album_id = a.album_id 
WHERE a.year_of_recording NOT BETWEEN '2020' AND '2020'
GROUP BY e.name
''').fetchall()
pprint(f'исполнители, которые не выпустили альбомы в 2020 году: {select_4}')

#5.названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
select_5 = connection.execute('''
SELECT c.title FROM collection_track ct
JOIN collection c ON ct.collection_id = c.collection_id
JOIN track t ON ct.track_id = t.track_id
JOIN album a ON t.album = album_id 
JOIN executor_album ea ON a.album_id = ea.album_id
JOIN executor e ON e.executor_id = ea.executor_id
WHERE e.name iLIKE '%%artist_6%%'
GROUP BY c.title
''').fetchall()
pprint(f'названия сборников, в которых присутствует конкретный исполнитель (выберите сами): {select_5}')

#6.название альбомов, в которых присутствуют исполнители более 1 жанра;
select_6 = connection.execute('''
SELECT a.title FROM executor_genre eg
JOIN genre g ON eg.genre_id = g.genre_id
JOIN executor e ON eg.executor_id = e.executor_id
JOIN executor_album ON executor_album.executor_id = e.executor_id 
JOIN album a ON executor_album.album_id = a.album_id
GROUP BY a.title
HAVING COUNT(g.genre_name) > 1
ORDER BY a.title
''').fetchall()
pprint(f'название альбомов, в которых присутствуют исполнители более 1 жанра: {select_6}')

#7.наименование треков, которые не входят в сборники;
select_7 = connection.execute('''
SELECT t.title FROM track t
JOIN collection_track ct ON ct.collection_id = t.track_id
WHERE ct.track_id is NULL
''').fetchall()
pprint(f'наименование треков, которые не входят в сборники: {select_7}')

#8.исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько);
select_8 = connection.execute('''
SELECT e.name, track.duration FROM track 
JOIN album a ON track.album = a.album_id 
JOIN executor_album ea ON a.album_id = ea.album_id
JOIN executor e ON e.executor_id = ea.executor_id
GROUP BY e.name, track.duration
HAVING track.duration = (SELECT min(duration) FROM track)
ORDER BY e.name
''').fetchall()
pprint(f'исполнителя(-ей), написавшего самый короткий по продолжительности трек: {select_8}')

#9.название альбомов, содержащих наименьшее количество треков.
select_9 = connection.execute('''
SELECT album.title FROM album 
JOIN track ON album_id = track.album
WHERE track.album IN (
SELECT album_id
FROM track
GROUP BY album_id
HAVING COUNT(track_id) = (
    SELECT COUNT(track_id)
    FROM track
    GROUP BY album_id
    ORDER BY count
    LIMIT 1
    )
)
ORDER BY album.title
''').fetchall()
pprint(f'название альбомов, содержащих наименьшее количество треков: {select_9}')