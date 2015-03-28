#! /bin/bash
set -e

repodir=../gnucash-copr
refspec=maint
upload_path=athene.kobaltwit.be:/var/www/html/gnucash.kobaltwit.be/copr

tempdir=$(mktemp -d /tmp/gnucash-copr.XXXXXX)
pushd "${tempdir}"
mkdir -p {BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMSSOURCE}
mkdir -p RPMS/{i686,x86_64,noarch}
popd

pushd "${repodir}"
echo "Update repository $repodir"
git checkout $refspec
git fetch
git reset --hard origin/$refspec
gc_version=$(grep AC_INIT configure.ac | perl -pe 's/.*([0-9]+\.[0-9]+\.[0-9]+).*\)/$1/ge')
gc_commit=$(git reflog | head -n1 | awk '{print $1}')
gc_full_version=${gc_version}-git.${gc_commit}
echo "Create source tarball gnucash-${refspec}.tar.bz2"
git archive ${gc_commit} --prefix "gnucash-${gc_version}" | bzip2 > "${tempdir}/SOURCES/gnucash-${refspec}.tar.bz2"
popd

perl -p -e"s#^Version: .*\$#Version: $gc_version#;" \
        -e"s#^Release: .*\$#Release: git.$gc_commit#" gnucash.spec > "${tempdir}/SPECS/gnucash.spec"

echo "Build source rpm gnucash-${gc_full_version}.src.rpm"
rpmbuild -D"%_topdir ${tempdir}" -bs ${tempdir}/SPECS/gnucash.spec
echo "Upload source rpm to $upload_path"
scp "${tempdir}/SRPMS/gnucash-${gc_full_version}.src.rpm" "${upload_path}"
echo "Start copr build"
copr-cli build gnucash-maint http://gnucash.kobaltwit.be/copr/gnucash-${gc_full_version}.src.rpm
rm -fr "${tempdir}"