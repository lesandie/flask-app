#!/bin/bash
set -o pipefail
set -o errexit
set -o errtrace
set -o nounset

# Store backup path
BACKUP="/mnt/backups/postgresql"
MFILE=""

# list of databases
#BBDDs="db1 db2 db3"
BBDD=""
BBDDs="simba baloo"

# Set PostgreSQL username and password
PGHOST="dbpostgres.xx.xx.xx"
PGUSER="postgres"
#variable PGPASSFILE
PGPASSFILE="/root/.pgpass"

# Paths for binary files
#TAR="/bin/tar"
PGDUMP="/usr/bin/pg_dump"
LOGGER="/usr/bin/logger"

# Commands
CMD_START="${LOGGER} $0: *** ${BBDD} backup started @ $(date) File: ${BACKUP}/${MFILE}***"
CMD_BACKUP="${PGDUMP} -h ${PGHOST} -U ${PGUSER} -w ${BBDD} > ${BACKUP}/${MFILE}"
CMD_DUMP="${PGDUMP} -h ${PGHOST} -U ${PGUSER} -w -Fc ${BBDD} > ${BACKUP}/${MFILE}"
CMD_END="${LOGGER} $0: *** ${BBDD} backup ended @ $(date) ***"

#Google cloud 
GCS_KEY_FILE_PATH="../.gcs_credentials"
BOTO_CONFIG_PATH="../.boto"
GCS_BUCKET="gs://pg_backup_revolut"

dir_exists() {
        # Make sure backup directory exists
        if [[ ! -d $BACKUP ]]; then
         mkdir -p "$BACKUP"
        fi
        cd "$BACKUP"
        # Remove this-day-last-week backup
        rm $(LC_ALL=en_US.utf8;date +'%A')_*
}


backup() {
        # Dump all databases. 
        for BBDD in "$BBDDs"; do
                # Log backup start time in /var/log/messages
                eval "$CMD_START"
                # Backup file name hostname.time.tar.gz
                MFILE="$(date +'%A')_$(date +'%F')_${BBDD}.sql"
                # SQL backup
                eval "$CMD_BACKUP"
                # backup.dmp
                MFILE="$(date +'%A')_$(date +'%F')_${BBDD}.dmp"
                eval "$CMD_DUMP"
                # Log backup end time in /var/log/messages
                eval "$CMD_END"
        done

}

upload_to_gcs() {
        if [[ ! "$GCS_BUCKET" =~ gs://* ]]; then
                GCS_BUCKET="gs://${GCS_BUCKET}"
        fi

        if [[ $GCS_KEY_FILE_PATH != "" ]]; then
        printf "[Credentials]\n \
                gs_service_key_file = %s\n \
                [Boto]\n \
                https_validate_certificates = True\n \
                [GoogleCompute]\n \
                [GSUtil]\n \
                content_language = en\n \
                default_api_version = 2\n \
                [OAuth2]\n" "$GCS_KEY_FILE_PATH" >> "$BOTO_CONFIG_PATH"
        fi
        echo "uploading backup archive to GCS bucket=$GCS_BUCKET"
        CMD="gsutil cp ${BACKUP_DIR}/${archive_name} ${GCS_BUCKET}"
        eval "$CMD"
}



cleanup() {
  rm "$BACKUP"/"$MFILE"
}

trap err ERR
dir_exists
backup
upload_to_gcs
cleanup

printf "backup done!"