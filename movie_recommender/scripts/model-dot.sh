#!/bin/bash

# ./manage.py graph_models -a > my_project.dot
# 
# # Create a PNG image file called my_project_visualized.png with application grouping
# ./manage.py graph_models -a -g -o my_project_visualized.png
# 
# # Same example but with explicit selection of pygraphviz or pydot
# ./manage.py graph_models --pygraphviz -a -g -o my_project_visualized.png
# ./manage.py graph_models --pydot -a -g -o my_project_visualized.png
# 
# # Create a dot file for only the 'foo' and 'bar' applications of your project
# ./manage.py graph_models foo bar > my_project.dot
# # Create a graph for only certain models
# ./manage.py graph_models -a -I Foo,Bar -o my_project_subsystem.png
# # Create a excluding certain models
# ./manage.py graph_models -a -X Foo,Bar -o my_project_sans_foo_bar.png


./manage.py graph_models booking_system > graphs/full.dot

./manage.py graph_models booking_system \
    -I Movie,CrewProfile,Crew,CastType,AggregateRating,Language \
    > graphs/movie.dot

./manage.py graph_models booking_system \
    -I Movie,User,Review,Genre,UserProfile,Gender\
    > graphs/user-movie.dot

./manage.py graph_models booking_system \
    -I Theater,City,Location,Seat,SeatType,Show,Movie,Screen\
    > graphs/show-movie.dot

./manage.py graph_models booking_system \
    -I Show,Seat,StatusType,Booking,Invoice,User\
    > graphs/booking.dot

./manage.py graph_models booking_system \
    -I Movie,Similar,PredictedRating,User\
    > graphs/recommendations.dot
