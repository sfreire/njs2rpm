njs2rpm
=======

N2R - convert NodeJS modules to RPM packages


## The problem



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
     
    ===================================================================================================
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

Fedora/RedHat typical approach is not to bundle dependencies in any of its packages, with some exceptions if justified.
Therefore, a module that depends on some other module will explicitly declare it as Requires in the RPM .spec file. This means that every NodeJS module packaged as RPM will just have their own files and require all dependencies, that must be installed in the system globally, each one as a package.
NodeJS community approach is quite different (see [NPM Faq](https://npmjs.org/doc/faq.html#I-installed-something-globally-but-I-can-t-require-it) ): every dependency should be installed locally, inside the application/module, meaning that dependencies are autocontained.

t

Contudo, tal como é visível no exemplo anterior, nem sempre é possível instalar um módulo de forma "limpa" dado que as dependências aos vários níveis podem colidir entre si. Assim, sugere-se a criação de pacotes do tipo "bundle" em que um módulo inclui todas as suas dependências, emitando assim o comportamento duma instalação autocontida usando o comado "npm". O pacote "bundle" ainda que não exponha as dependências embebidas, enumera-as nos Provides do RPM usando o prefixo "bundled-" para se conseguir identificar claramente as versões dos módulos que contém.

 


## Examples


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
    
    $ rpm --provides -qp /home/sergio/rpmbuild/RPMS/noarch/nodejs-express-3.4.4-1.el6.noarch.rpm
    npm(express) = 3.4.4
    nodejs-express = 3.4.4-1.el6

## Syntax

    NJS2RPM v1.0.0 - NodeJs module to RPM converter by Sergio Freire <sergio-s-freire@ptinovacao.pt>
     Usage: njs2rpm <name> <version> <release> <single|bundle> <spec|rpm> [template]
            name: NodeJS module name
            version: module version in X.Y.Z format
            release: RPM's release
            single: just package the module and not its dependencies (RH behaviour)
            bundle: bundle all dependencies inside the module
            spec: just create the .spec file
            rpm: create the .spec and the RPM file(s)
            template (optional): RPM .spec template to use; by default, provided default.n2r
     Examples:
            njs2rpm uglify-js 2.4.1 1 single rpm
            njs2rpm uglify-js 2.4.1 1 bundle rpm
            njs2rpm express 3.4.4 1 bundle spec mytemplate.n2r


## References
- https://fedoraproject.org/wiki/Packaging:Node.js
- https://npmjs.org/doc/faq.html#I-installed-something-globally-but-I-can-t-require-it
- https://fedoraproject.org/wiki/User:Lkundrak/NodeJS#Packaging_node.js_in_Fedora