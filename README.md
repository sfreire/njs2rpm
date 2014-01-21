njs2rpm
=======

NJS2RPM - convert NodeJS modules to RPM packages (by Sergio Freire)

A simple Bash script to build RPMs of any available NodeJS module, any version.
It fetches the source from NPM Registry and builds the RPM. Simple, isn't it?

No more NodeJS modules installed ad-hoc using "npm".

## Features
- supports RHEL6 and RHEL5/Centos5 (yes, RHEL5!) - runs and build RPM packages on these systems
- simple creation of RPM obtaining sources directly from [NPM Registry](npmjs.org), of any package and version available!
- does not require Perl, Python, Ruby and a bulk of dependencies in order to run! It's made in shell script: "BASH" to the rescue!
- supports [NodeJS packaging guidelines used in Fedora/EPEL](https://fedoraproject.org/wiki/Packaging:Node.js) (and upcoming RedHat versions) for building clean ("single") packages
- supports the creation of "bundle" packages with all dependencies pre-bundled, overcoming the "limitation" of some modules with dependency problems!
- supports RPM (or .spec) creation based on template files in order to customized the generated RPM

Examples:
		
        njs2rpm uglify-js 2.4.1 1 single rpm
		njs2rpm uglify-js 2.4.1 1 bundle rpm
        njs2rpm express 3.4.4 1 bundle spec mytemplate.n2r


## Syntax

    NJS2RPM v1.0.2 - NodeJs module to RPM converter by Sergio Freire <sergio-s-freire@ptinovacao.pt>
     Usage: njs2rpm <name> <version> <release> <single|bundle> <spec|rpm> [template]
            name: NodeJS module name
            version: module version in X.Y.Z format
            release: RPM's release
            single: just package the module and not its dependencies (RH behaviour)
            bundle: bundle all dependencies inside the module
            spec: just create the .spec file
            rpm: create the .spec and the RPM file(s)
            template (optional): RPM .spec template to use; by default, provided default.n2r



## The dependencies problem

Bellow, you can see the "express" framework installed locally using "npm install express". It's clear that "express" requires a lot of modules, a few directly and a lot of them indirectly (i.e. modules that require some other modules, so on, so on).

    $ tree -d
    .
    └── express
        ├── bin
        ├── lib
        │   └── router
        └── node_modules
            ├── buffer-crc32
            │   └── tests
            ├── commander
            │   └── node_modules
            │       └── keypress
            ├── connect
            │   ├── lib
            │   │   ├── middleware
            │   │   │   └── session
            │   │   └── public
            │   │       └── icons
            │   └── node_modules
            │       ├── bytes
            │       ├── methods
            │       ├── multiparty
            │       │   ├── examples
            │       │   ├── node_modules
            │       │   │   ├── readable-stream
            │       │   │   │   ├── examples
            │       │   │   │   ├── lib
            │       │   │   │   ├── node_modules
            │       │   │   │   │   ├── core-util-is
            │       │   │   │   │   │   └── lib
            │       │   │   │   │   └── debuglog
            │       │   │   │   └── test
            │       │   │   │       ├── fixtures
            │       │   │   │       └── simple
            │       │   │   └── stream-counter
            │       │   │       └── test
            │       │   └── test
            │       │       ├── fixture
            │       │       │   ├── file
            │       │       │   ├── http
            │       │       │   │   ├── encoding
            │       │       │   │   ├── no-filename
            │       │       │   │   ├── preamble
            │       │       │   │   ├── special-chars-in-filename
            │       │       │   │   └── workarounds
            │       │       │   └── js
            │       │       └── standalone
            │       ├── negotiator
            │       │   ├── examples
            │       │   ├── lib
            │       │   └── test
            │       ├── pause
            │       ├── qs
            │       ├── raw-body
            │       └── uid2
            ├── cookie
            │   └── test
            ├── cookie-signature
            ├── debug
            │   ├── example
            │   └── lib
            ├── fresh
            ├── methods
            ├── mkdirp
            │   ├── examples
            │   └── test
            ├── range-parser
            └── send
                ├── lib
                └── node_modules
                    └── mime
                        └── types
    70 directories
     

The dependency problem arises when some module, at some level, requires some other module in a conflicting version. Looking a bit further at "express" v3.4.4 once again, it can be seen that "express" directly requires "methods = v0.1.0". But "connect", which is also a direct dependency, requires "methods = v0.0.1". This is just an example, which may be HUGE whenever using lots of modules in your NodeJS apps. If we tried to follow the typical RedHat guidelines for packaging "express v3.4.4", it simply would not be possible to install "express" (unless we patched it manually and correctly... and tested it!).

     express@3.4.4 node_modules/express
    ├── methods@0.1.0
    ├── cookie-signature@1.0.1
    ├── range-parser@0.0.4
    ├── fresh@0.2.0
    ├── buffer-crc32@0.2.1
    ├── cookie@0.1.0
    ├── debug@0.7.2
    ├── mkdirp@0.3.5
    ├── send@0.1.4 (mime@1.2.11)
    ├── commander@1.3.2 (keypress@0.1.0)
    └── connect@2.11.0 (methods@0.0.1, uid2@0.0.3, pause@0.0.1, raw-body@0.0.3, qs@0.6.5, bytes@0.2.1, negotiator@0.3.0, multiparty@2.2.0)

## Rationale

Fedora/RedHat typical approach is [not to bundle dependencies](https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries) in any of its packages, with some exceptions if justified.
Therefore, a module that depends on some other module will explicitly declare it as Requires in the RPM .spec file. This means that every NodeJS module packaged as RPM will just have their own files and require all dependencies, that must be installed in the system globally, each one as a package.
NodeJS community approach is quite different (see [NPM Faq](https://npmjs.org/doc/faq.html#I-installed-something-globally-but-I-can-t-require-it) ): every dependency should be installed locally, inside the application/module, meaning that dependencies are autocontained.

As seen earlier with the "express" framework example, we need another way of building RPM packages for NodeJS modules. Thus, the "bundle" packaging is introduced.
A "bundle" package solves the problem by containing all dependencies of the given module. Basically, it follows the same principle used whenever installing Node modules with "npm install ...".
A "bundle" package does not expose the bundled dependencies as typical "npm(<module_name>)" Provides in the RPM, since the bundled modules cannot be used by third party apps or modules. Nevertheless, in order to not make things obscure and make clear what are the bundled dependent modules and their respective versions, all these modules are "visible" as Provides using the "bundled-..." prefix (e.g. "bundled-npm(methods) = 0.1.0"). Note that an app or modules MUST NOT require these type of dependencies.
 
### Summary

    +--------+----------------------+---------------------+-----------------------------+
    |  Type  |       RPM name       |      Provides       |          Requires           |
    +--------+----------------------+---------------------+-----------------------------+
    | Single | nodejs-<name>        | npm(<name>)         | npm(<dep1>)                 |
    |        |                      |                     | ...                         |
    |        |                      |                     | npm(<depM>)                 |
    | Bundle | nodejs-bundle-<name> | npm(<name>)         | (no deps as Requires)       |
    |        |                      |                     |                             |
    |        |                      | bundled-npm(<dep1>) |                             |
    |        |                      | ...                 |                             |
    |        |                      | bundled-npm(<depN>) |                             |
    +--------+----------------------+---------------------+-----------------------------+

## Examples

### single package
This example concerns the "express" framework v3.4.4, using the "clean way" (i.e. packaging guidelines typically followed by RH).

	$ njs2rpm express 3.4.4 1 single rpm

    $ rpm --provides -qp /home/sergio/rpmbuild/RPMS/noarch/nodejs-express-3.4.4-1.el6.noarch.rpm
    
    npm(express) = 3.4.4
    nodejs-express = 3.4.4-1.el6
    
    
    $ rpm --requires -qp /home/sergio/rpmbuild/RPMS/noarch/nodejs-express-3.4.4-1.el6.noarch.rpm
    
    rpmlib(FileDigests) <= 4.6.0-1
    rpmlib(PayloadFilesHavePrefix) <= 4.0-1
    rpmlib(CompressedFileNames) <= 3.0.4-1
    rpmlib(VersionedDependencies) <= 3.0.3-1
    nodejs(engine)
    npm(buffer-crc32) = 0.2.1
    npm(cookie-signature) = 1.0.1
    npm(methods) = 0.1.0
    npm(mkdirp) = 0.3.5
    npm(send) = 0.1.4
    npm(commander) = 1.3.2
    npm(cookie) = 0.1.0
    npm(connect) = 2.11.0
    npm(fresh) = 0.2.0
    npm(debug)
    npm(range-parser) = 0.0.4
    /usr/bin/env
    rpmlib(PayloadIsXz) <= 5.2-1
    


### bundle package
This example concerns the "uglify-js" famous javascript packer v2.4.1, using the "bundle" approach (i.e. all dependencies bundled).

	$ njs2rpm uglify-js 2.4.1 1 bundle rpm
    
    $ rpm --provides  -q nodejs-bundle-uglify-js
    
    bundled-npm(amdefine) = 0.1.0
    bundled-npm(async) = 0.2.9
    bundled-npm(optimist) = 0.3.7
    bundled-npm(source-map) = 0.1.31
    bundled-npm(uglify-to-browserify) = 1.0.1
    bundled-npm(wordwrap) = 0.0.2
    npm(uglify-js) = 2.4.1
    nodejs-bundle-uglify-js = 2.4.1-1.ptin.el6
    
    
    $ rpm --requires  -q nodejs-bundle-uglify-js
    
    /usr/bin/env
    nodejs(engine)
    rpmlib(CompressedFileNames) <= 3.0.4-1
    rpmlib(FileDigests) <= 4.6.0-1
    rpmlib(PayloadFilesHavePrefix) <= 4.0-1
    rpmlib(VersionedDependencies) <= 3.0.3-1
    rpmlib(PayloadIsXz) <= 5.2-1

## NJS2RPM install dependencies
- "redhat-rpm-config", tar, coreutils
- "nodejs-devel". For RHEL6, RPM is at EPEL 6 repository; for RHEL5, see NodeJS notes bellow.
- "nodejs-packaging" RPM macros. For RHEL6, RPM is at EPEL 6 repository; for RHEL5  see [my patches for nodejs-packaging](https://github.com/sfreire/nodejs-packaging)
- "npm". For RHEL6, RPM is at EPEL 6 repository; for RHEL5 see NodeJS notes bellow.

### NodeJS and RHEL5/Centos5
See my [patches to build NodeJS for RHEL5](https://github.com/sfreire/nodejs-rpm-centos5), similarly to the RPMs provides by the Fedora/EPEL community for RHEL6.

## Unsupported
- creation of native/linked modules (yet!)

## Changelog
    * Thu Nov  8 2013 Sergio Freire <sergio-s-freire@ptinovacao.pt> - 1.0.1-1
    - changed default template so RPM macro _rpmconfigdir points to 32 bit libs diretory. have to fix this better
    - disabled debuginfo packages on default template
    - avoid stderr messages of tar in RHEL5
    * Thu Nov  7 2013 Sergio Freire <sergio-s-freire@ptinovacao.pt> - 1.0.0-4
    - describe better the package description
    - removed my email from the default template
    * Thu Nov  7 2013 Sergio Freire <sergio-s-freire@ptinovacao.pt> - 1.0.0-3
    - change name from n2r to njs2rpm
    - included LICENSE
    * Wed Nov  6 2013 Sergio Freire <sergio-s-freire@ptinovacao.pt> - 1.0.0-2
    - first public release, compatible with RHEL5 and RHEL6

## License
This software is provided under [LGPL v2.1](https://raw.github.com/sfreire/njs2rpm/master/LICENSE).

## References
- https://fedoraproject.org/wiki/Node.js
- https://fedoraproject.org/wiki/Packaging:Node.js
- https://npmjs.org/doc/faq.html#I-installed-something-globally-but-I-can-t-require-it
- https://fedoraproject.org/wiki/User:Lkundrak/NodeJS#Packaging_node.js_in_Fedora
