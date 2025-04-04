#!/bin/bash

if [[ -f 'config/config.sh' ]]; then
    source config/config.sh
fi


FOP_OPTS="${fop_opts}" "${fop_bin}" -nocs -c "${fop_conf}" "${fo_obj}" "${pdf_obj}"


#"${fop_bin}" -c "${fop_conf}" "${fo_obj}" "${pdf_obj}"
