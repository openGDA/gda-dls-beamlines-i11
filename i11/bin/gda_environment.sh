#!/bin/sh
# This script assumes that $BEAMLINE is set (e.g. i02, i18, b16) if not exit...

# **** DO NOT EDIT THIS SCRIPT AS IT MAY BE AUTOMATICALLY OVERWRITTEN *****

if [ ! -n "$BEAMLINE" ]; 
then
  echo "Please set BEAMLINE environment variable."
  exit 1
fi
export SOFTWAREFOLDER=dls
export GDA_ROOT=/$SOFTWAREFOLDER/$BEAMLINE/software/gda
export GDA_CONFIG=${GDA_ROOT}/config
export GDA_DATADIR=/$SOFTWAREFOLDER/$BEAMLINE/data

#IDL VM settings
export IDL_DIR=/$SOFTWAREFOLDER/$BEAMLINE/software/itt/idl
export IDL_DLM_PATH=${IDL_DIR}/bin/bin.linux.x86
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${IDL_DLM_PATH}
export PATH=$PATH:${IDL_DLM_PATH}
export IDL_PATH=${GDA_CONFIG}/idlobjects:${IDL_DIR}/lib/wavelet/data:${IDL_DIR}/lib/wavelet/source:${IDL_DIR}/lib/utilities:${IDL_DIR}/lib/imsl:${IDL_DIR}/lib/obsolete:${IDL_DIR}/lib/itools/ui_widgets:${IDL_DIR}/lib/itools/framework:${IDL_DIR}/lib/itools/components:${IDL_DIR}/lib/itools:${IDL_DIR}/lib/bridges:${IDL_DIR}/lib/dicomex:${IDL_DIR}/lib/hook:${IDL_DIR}/lib:${IDL_DIR}/examples/demo/demodata:${IDL_DIR}/examples/demo/demosrc:${IDL_DIR}/examples/demo/demoslideshows/slideshowsrc:${IDL_DIR}/examples/demo:${IDL_DIR}/examples/data:${IDL_DIR}/examples/imsl:${IDL_DIR}/examples/widgets/wexmast:${IDL_DIR}/examples/widgets:${IDL_DIR}/examples/HP_TIFF:${IDL_DIR}/examples/mjpeg2000:${IDL_DIR}/examples/doc/sdf:${IDL_DIR}/examples/doc/plot:${IDL_DIR}/examples/doc/shaders:${IDL_DIR}/examples/doc/image:${IDL_DIR}/examples/doc/utilities:${IDL_DIR}/examples/doc/signal:${IDL_DIR}/examples/doc/widgets:${IDL_DIR}/examples/doc/objects:${IDL_DIR}/examples/doc/language:${IDL_DIR}/examples/doc/file_io:${IDL_DIR}/examples/doc/itools:${IDL_DIR}/examples/doc/bridges:${IDL_DIR}/examples/doc/dicom:${IDL_DIR}/examples/ogc/wms:${IDL_DIR}/examples/ogc/wcs:${IDL_DIR}/examples/misc:${IDL_DIR}/examples
export IDL_JAVA_WRAPPER_CLASS=${GDA_CONFIG}/idlobjects

export CLASSPATH="$CLASSPATH:${IDL_DIR}/resource/bridges/export/java/javaidlb.jar:${IDL_JAVA_WRAPPER_CLASS}"

unset ANT_HOME
unset JAVA_HOME
unset JYTHON_HOME
unset SVN_HOME

export PATH=/$SOFTWAREFOLDER/$BEAMLINE/software/gda/config/bin:/$SOFTWAREFOLDER/$BEAMLINE/software/gda/config/pytools/src:/dls_sw/dasc/bin/iKittenScripts:/$SOFTWAREFOLDER/$BEAMLINE/bin:$PATH

if [ -f /$SOFTWAREFOLDER/${BEAMLINE}/software/gda/builder/set_tools.sh ]; then
	cd /$SOFTWAREFOLDER/${BEAMLINE}/software/gda/builder
	source set_tools.sh > ~/.set_tools_report.txt
	cd ~
fi

# If for whatever reason GDA_Launchers failed to be created on user login, this will create it when user open a terminal.
case $DISPLAY in 
	:0.0|${BEAMLINE}*:0)
		( cd $HOME/Desktop && test -e "GDA_Launchers" || ln -s /usr/local/etc/"GDA_Launchers" . ) > /dev/null 2>&1
		( cd $HOME/Desktop && test -e "${BEAMLINE}_Launchers" || ln -s /usr/local/etc/"${BEAMLINE}_Launchers" . ) > /dev/null 2>&1
		;;
	*)
		:
		;;
esac




