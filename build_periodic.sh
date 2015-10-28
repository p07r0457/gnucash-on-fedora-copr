#! /bin/bash
set -e

code_package=gnucash
docs_package=gnucash-docs
code_repodir=../${code_package}-copr
docs_repodir=../${docs_package}-copr
refspec=master
copr_repo=${code_package}-${refspec}

if [ -f ./custom.sh ]
then
    . ./custom.sh
fi

. ./functions.sh

make_tmp_dir

# Prepare the code src rpm
package=${code_package}
repodir=${code_repodir}
prepare_repo
get_versions

code_curr_rev=${gc_commit}
touch ./code_last_rev
code_last_rev=$(cat ./code_last_rev)
if [[ "$code_curr_rev" != "$code_last_rev" ]]
then
    build_code=yes
    code_full_version=${gc_full_version}
    create_specfile
    create_tarball
    create_srpm
else
    build_code=no
fi

# Prepare the docs src rpm
package=${docs_package}
repodir=${docs_repodir}
prepare_repo
get_versions

docs_curr_rev=${gc_commit}
touch ./docs_last_rev
docs_last_rev=$(cat ./docs_last_rev)
if [[ "$docs_curr_rev" != "$docs_last_rev" ]]
then
    build_docs=yes
    docs_full_version=${gc_full_version}
    create_specfile
    create_tarball
    create_srpm
else
    build_docs=no
fi

# Start all necessary builds in parallel
if [[ $build_code == yes ]] || [[ $build_docs == yes ]]
then
    echo "Start copr build(s) and wait for them to finish"
else
    echo "No changes since last successful run - no builds started"
fi

if [[ $build_code == yes ]]
then
    #rpmbuild -D"%_topdir ${tempdir}" --rebuild ${tempdir}/SRPMS/${code-package}-${code_full_version}.src.rpm
    copr-cli build --nowait ${copr_repo} "${tempdir}/SRPMS/${code_package}-${code_full_version}.src.rpm" | tee "${tempdir}/code_build.txt"
    code_build_id=$(awk '/^Created builds:/ { print $3}' "${tempdir}/code_build.txt")
fi
if [[ $build_docs == yes ]]
then
    #rpmbuild -D"%_topdir ${tempdir}" --rebuild ${tempdir}/SRPMS/${docs-package}-${docs_full_version}.src.rpm
    copr-cli build --nowait ${copr_repo} "${tempdir}/SRPMS/${docs_package}-${docs_full_version}.src.rpm" | tee "${tempdir}/docs_build.txt"
    docs_build_id=$(awk '/^Created builds:/ { print $3}' "${tempdir}/docs_build.txt")
fi

rm -fr "${tempdir}"

# Wait for the builds to finish
code_status="first_loop"
docs_status="first_loop"
while [[ "$code_status" != "succeeded" ]] && [[ "$code_status" != "failed" ]] && \
      [[ "$docs_status" != "succeeded" ]] && [[ "$docs_status" != "failed" ]]
do
    sleep 60

    if [[ $build_code == yes ]]
    then
        code_status=$(copr-cli status $code_build_id)
        if [[ $? -ne 0 ]]
        then
            code_status=failed
        fi
    fi
    if [[ $build_docs == yes ]]
    then
        docs_status=$(copr-cli status $docs_build_id)
        if [[ $? -ne 0 ]]
        then
            docs_status=failed
        fi
    fi
done

if [[ $build_code == yes ]]
then
    echo "Code build result: $code_status"
    if [[ "$code_status" == "succeeded" ]]
    then
        echo -n $code_curr_rev > ./code_last_rev
    fi
fi
if [[ $build_docs == yes ]]
then
    echo "Docs build result: $docs_status"
    if [[ "$docs_status" == "succeeded" ]]
    then
        echo -n $docs_curr_rev > ./docs_last_rev
    fi
fi
