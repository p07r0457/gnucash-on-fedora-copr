#! /bin/bash
set -e

code_package=gnucash
docs_package=gnucash-docs
code_repodir=../${code_package}-copr
docs_repodir=../${docs_package}-copr
refspec=maint
copr_repo=${code_package}-${refspec}

. ./functions.sh

make_tmp_dir

# First prepare the code src rpm
package=${code_package}
repodir=${code_repodir}
prepare_repo
get_versions
code_full_version=${gc_full_version}
create_specfile
create_tarball
create_srpm

# Next prepare the docs src rpm
package=${docs_package}
repodir=${docs_repodir}
prepare_repo
get_versions
docs_full_version=${gc_full_version}
create_specfile
create_tarball
create_srpm

echo "Start copr build"
#rpmbuild -D"%_topdir ${tempdir}" --rebuild ${tempdir}/SRPMS/${code-package}-${code_full_version}.src.rpm
#rpmbuild -D"%_topdir ${tempdir}" --rebuild ${tempdir}/SRPMS/${docs-package}-${docs_full_version}.src.rpm
copr-cli build ${copr_repo} "${tempdir}/SRPMS/${code_package}-${code_full_version}.src.rpm"
copr-cli build ${copr_repo} "${tempdir}/SRPMS/${docs_package}-${docs_full_version}.src.rpm"

rm -fr "${tempdir}"
