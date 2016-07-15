#!/bin/bash
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

srv(){

    sudo dd of=/etc/init/sfc-generator.conf <<EOF
# SFC Demo generator
#

description  "SFC Demo generator"

start on runlevel [2345]
stop on runlevel [!2345]


script
    while true ;  do
        dmesg -T true | nc $1 8022 || true
    done
end script
EOF
    sudo initctl start sfc-generator
}


rcv(){

    sudo dd of=/etc/init/sfc-receiver.conf <<EOF
# SFC Demo receiver
#

description  "SFC Demo receiver"

start on runlevel [2345]
stop on runlevel [!2345]

script
    while true ;  do
        nc -l 8022 >/dev/null || true
    done
end script
EOF
    sudo initctl start sfc-receiver

}

sfc(){
    sudo apt-get -y install debconf-utils
    echo "ntop ntop/admin_password_again password r00tme
ntop ntop/admin_password password r00tme
ntop ntop/user string ntop
ntop ntop/interfaces string eth0
" | sudo debconf-set-selections
    sudo apt-get -y install ntop

}

sudo apt-get update
case "$1" in
    "sfc-app" )
        sfc
    ;;
    "left-endpoint" )
        srv $3
    ;;
    "right-endpoint" )
        rcv
esac


