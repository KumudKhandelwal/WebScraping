var { Readability } = require('@mozilla/readability');
var { JSDOM } = require('jsdom');
const yargs = require('yargs')
fs  = require('fs');

// Lecture des arguments
const argv = yargs.
    command('batch', "Utilise readability sur tous les éléments d'un dossier", {
        // Dossier où l'on place nos HTML d'entrée
        input_dir: {
            description: "Dossier d'entrée",
            alias: 'input',
            type: 'text',
        },
        // Dossier où sont placés les fichiers de sortie
        output_file: {
            description: "Dossier de sortie",
            alias: 'output',
            type: 'text',
        }
    })
    .argv;


// 
if (argv._.includes('batch')) {
    // Récupération des chemins
    let input_dir = argv.input_file;
    let output_file = argv.output_file;
    let input_dir_list = fs.readdirSync(input_dir);

    // Options de readability

    options = {
        resources: "usable"
    };
    // Parcours des fichiers HTML + transformation
    for (i in input_dir_list){
        console.log(input_dir_list[i]);
        // Chemins des fichiers d'entrée/Sortie
        let file_in = input_dir.concat(input_dir_list[i]);
        let file_out = output_file.concat(input_dir_list[i]);
        JSDOM.fromFile(file_in, options).then(function (dom) {
        // On applique readability au document
        let window = dom.window,
        document = window.document;
        let reader = new Readability(document);
        let article = reader.parse();
        if (article.textContent != null || article.textContent.length != 0){
            fs.writeFile(file_out, article.textContent.trim().replace(/\t/g, ''), function (err) {
                if (err){
                    console.log(err);
                }
                 
            });
        }
        
        //console.log(article.textContent)
    
    }).catch (function (e) {
        console.log(e);
    });
    };
}

