# Build scripts for Fedora Copr #

This repository offers some code to enable building Fedora rpm packages
for gnucash and gnucash-docs on the Fedora Copr infrastructure.

**IMPORTANT** These packages are not intended to replace the packages that
already ship with Fedora. They are generated as a means to easily test
changes that have landed in the gnucash code and documentation that has
not been released yet.

Again: these packages are not release quality for several reasons:

1. They will contain features that have not been released yet and that
   may or may not have been throuroughly tested, or may not even be complete
   just yet.

2. The script that builds these packages does not use the same source tar ball
   as the releases do. Releases start from a tar ball generated by running
   make dist(check) on the source repository. The copr packages are created
   from a tar ball generated by running git archive on the source repository
   and manually tweaking a few build steps. So no distcheck is run for these
   packages !

However, now that it's clearly stated the packages are meant purely for
testing unreleased features, here's how to use these scripts.

1. [Create a copr repo](https://copr.fedoraproject.org/). The script will assume a default name of
   'gnucash-_branchname_', like gnucash-maint or gnucash-master (for the
   two default branches). If you choose another name, you can override the
   defaults by including a custom.sh script.

2. Install copr-cli and make sure it can access your copr-repy by installing
   the proper [api key](https://copr.fedoraproject.org/api/).

3. Clone this repo:  
   git clone https://github.com/Gnucash/gnucash-on-fedora-copr

4. Clone the gnucash repo  
   git clone https://github.com/Gnucash/gnucash

5. Clone the gnucash-docs repo  
   git clone https://github.com/Gnucash/gnucash-docs

6. If needed copy custom.sh-sample to custom.sh and override the variables
   found in there are desired/needed (for example if your repos are in 
   another location than default, or using non-default names/branches).

7. cd into the gnucash-on-fedora-copr repository and run  
   ./build_peridoc.sh

That should be it !

## Notes ##

* The script will only build the packages if there are changes in the source
  repositories since the last build.
* The copr interface api key expires after 180 days (about 6 months). At that
  moment you will have to renew it by connecting to the [api website](https://copr.fedoraproject.org/api/)  again.
