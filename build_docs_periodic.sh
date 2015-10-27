#! /bin/bash
set -e

repodir=../gnucash-docs-copr
refspec=maint
upload_path=athene.kobaltwit.be:/var/www/html/gnucash.kobaltwit.be/copr

tempdir=$(mktemp -d /tmp/gnucash-docs-copr.XXXXXX)
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
gc_full_version=${gc_version}-nightly.git.${gc_commit}

echo "Create source tarball gnucash-docs-${refspec}.tar.bz2"
git archive ${gc_commit} --prefix "gnucash-docs-${gc_version}/" > "${tempdir}/SOURCES/gnucash-docs-${refspec}.tar"
popd

bzip2 "${tempdir}/SOURCES/gnucash-docs-${refspec}.tar"

rm -fr "gnucash-docs-${gc_version}"

perl -p -e"s#^Version: .*\$#Version: $gc_version#;" \
        -e"s#^Release: .*\$#Release: nightly.git.$gc_commit#" gnucash-docs.spec > "${tempdir}/SPECS/gnucash-docs.spec"

echo "Build source rpm gnucash-docs-${gc_full_version}.src.rpm"
rpmbuild -D"%_topdir ${tempdir}" -bs ${tempdir}/SPECS/gnucash-docs.spec

echo "Start copr build"
#rpmbuild -D"%_topdir ${tempdir}" --rebuild ${tempdir}/SRPMS/gnucash-docs-${gc_full_version}.src.rpm
copr-cli build gnucash-maint "${tempdir}/SRPMS/gnucash-docs-${gc_full_version}.src.rpm"
rm -fr "${tempdir}"
