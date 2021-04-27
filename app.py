import os
from sqlalchemy.orm.session import Session
import streamlit as st
from PIL import Image
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import *
import db

def open_db():
    engine = create_engine("sqlite:///db.sqlite3")
    Session = sessionmaker(bind=engine)
    return Session()

if not os.path.exists("uploads"):
    os.mkdir(UPLOAD_FOLDER)

st.title(TITLE)
choice = st.radio("select options",MENU)

if choice =='upload image':
    imgdata = st.file_uploader("select an image",type=['jpg','png'])
    if imgdata:
        # load image as a Pillow object
        im = Image.open(imgdata)
        # create a address for image path
        path = os.path.join(UPLOAD_FOLDER,imgdata.name)
        # save file to upload folder
        im.save(path,format=imgdata.type.split('/')[1])
        # saves info to db
        sess = open_db()
        imdb = db.Image(path=path)
        sess.add(imdb)
        sess.commit()
        sess.close()
        # show a msg
        st.success('image uploaded successfully')

if choice == 'view uploads':
    # open the database
    sess = open_db()
    # get all the images from the image table
    images = sess.query(db.Image).all()
    # close database
    sess.close()
    
    # show the image names in sidebar to select one
    select_img = st.sidebar.radio("select an image",images)
    if os.path.exists(select_img.path):
        # load the image obj using selected image path
        im = Image.open(select_img.path)
        # show the image, fill the area available
        st.image(im,use_column_width=True)

if choice =='remove uploads':
    sess = open_db()
    images = sess.query(db.Image).all()
    sess.close()
    
    # show the image names in sidebar to select one
    select_img = st.sidebar.radio("select an image",images)
    if select_img and st.button("remove"):
        sess = open_db()
        sess.query(db.Image).filter(db.Image.id==select_img.id).delete()
        if os.path.exists(select_img.path):
            os.unlink(select_img.path)
        sess.commit()
        sess.close()




