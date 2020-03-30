#/bin/bash

D_STR=$(date "+%Y-%m-%d")

while getopts v:d: option
do
case "${option}"
in
v) VERSION=${OPTARG};;
d) DATE=${OPTARG};;
esac
done

echo "==========================="
echo "Building Sensu Go (Open Source)"
echo "Version Number: $VERSION"

go build -ldflags '-X "github.com/sensu/sensu-go/version.Version='`echo $VERSION`'" -X "github.com/sensu/sensu-go/version.BuildDate='`date "+%Y-%m-%d"`'"' -o bin/sensu-agent ./cmd/sensu-agent
go build -ldflags '-X "github.com/sensu/sensu-go/version.Version='`echo $VERSION`'" -X "github.com/sensu/sensu-go/version.BuildDate='`date "+%Y-%m-%d"`'"' -o bin/sensu-backend ./cmd/sensu-backend
go build -ldflags '-X "github.com/sensu/sensu-go/version.Version='`echo $VERSION`'" -X "github.com/sensu/sensu-go/version.BuildDate='`date "+%Y-%m-%d"`'"' -o bin/sensuctl ./cmd/sensuctl
echo "Build Done."
echo "==========================="
