#!/bin/bash

#CONFIGS="epel-5-i386 epel-6-i386"
CONFIGS="ptin-5-i386 ptin-6-i386"
TMPDIR=njs2rpm$(date +%s)
EPELPKGURL=http://ftp.tu-chemnitz.de/pub/linux/fedora-epel/5/i386/epel-release-5-4.noarch.rpm

function cleanup {
 rm -rf $TMPDIR
 exit 1
}

rm -rf RPMS
mkdir -p $TMPDIR
cp * $TMPDIR

for CONFIG in $CONFIGS
do
 mock -r $CONFIG --init
 [ $? -eq 0 ] || cleanup

 if [ "$CONFIG" == "ptin-5-i386" ] || [ "$CONFIG" == "epel-5-i386" ]
 then
	mock -r $CONFIG --install $EPELPKGURL
	[ $? -eq 0 ] || exit 1
	mock -r $CONFIG --install python26
	[ $? -eq 0 ] || exit 1
 fi

 mock -r $CONFIG --copyin $TMPDIR /tmp/$TMPDIR
 [ $? -eq 0 ] || cleanup
 mock -r $CONFIG --shell ". /etc/profile; cd /tmp/$TMPDIR; make rpm"
 [ $? -eq 0 ] || cleanup
 mock -r $CONFIG --copyout /tmp/$TMPDIR/rpmbuild/RPMS RPMS/$CONFIG
 [ $? -eq 0 ] || cleanup
done

rm -rf $TMPDIR
