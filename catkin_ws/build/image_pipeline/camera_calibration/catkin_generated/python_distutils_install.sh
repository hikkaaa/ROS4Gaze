#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/kai/catkin_ws/src/image_pipeline/camera_calibration"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/kai/catkin_ws/install/lib/python3.9/site-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/kai/catkin_ws/install/lib/python3.9/site-packages:/home/kai/catkin_ws/build/lib/python3.9/site-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/kai/catkin_ws/build" \
    "/home/kai/miniforge3/envs/ros_env/bin/python3.9" \
    "/home/kai/catkin_ws/src/image_pipeline/camera_calibration/setup.py" \
    egg_info --egg-base /home/kai/catkin_ws/build/image_pipeline/camera_calibration \
    build --build-base "/home/kai/catkin_ws/build/image_pipeline/camera_calibration" \
    install \
    --root="${DESTDIR-/}" \
     --prefix="/home/kai/catkin_ws/install" --install-scripts="/home/kai/catkin_ws/install/bin"
