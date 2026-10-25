"""NEET chapter list used to tag every mock-test question with its chapter (build time, no AI needed).

Each entry: (id, name, subject, extra names a student may type (English / Hinglish), keywords found in questions).
A keyword is matched as a whole word (words of 6+ letters match as a word prefix, so "glomerul" matches
glomerulus / glomerular). The chapter with the most distinct keyword hits wins.
"""

CHAPTERS = [
# ---------------------------------------------------------------- BIOLOGY
("living-world", "The Living World", "Biology",
 "living world,taxonomy,nomenclature,taxonomic hierarchy",
 "taxon,taxonomy,taxonomic,nomenclature,binomial,herbarium,systematics,monograph,hierarch,botanical garden,zoological park,"
 "museum,taxonomical aids,icbn,iczn,genus,homo sapiens,flora,fauna,taxa,taxon,rank,classification categories"),
("biological-classification", "Biological Classification", "Biology",
 "biological classification,five kingdom,monera,protista,fungi,kingdom classification",
 "monera,protista,fungi,fungus,whittaker,archaebacteria,eubacteria,cyanobacteria,mycoplasma,virus,viroid,prion,lichen,mycorrhiza,"
 "dinoflagellate,euglenoid,diatom,slime mould,zygomycetes,ascomycetes,basidiomycetes,deuteromycetes,phycomycetes,five kingdom,"
 "chrysophyte,protozoan,bacteriophage,heterocyst,bacteria,mycelium,hyphae,yeast,penicillium,mushroom,rhizopus,puccinia,neurospora,"
 "plasmodium,amoeboid,ciliated protozoan,gonyaulax,archaea,halophile,methanogen,thermoacidophile"),
("plant-kingdom", "Plant Kingdom", "Biology",
 "plant kingdom,algae,bryophytes,pteridophytes,gymnosperms,plantae",
 "algae,algal,bryophyte,pteridophyte,gymnosperm,angiosperm,liverwort,moss,fern,red algae,brown algae,green algae,chlorophyceae,"
 "phaeophyceae,rhodophyceae,sporophyte,gametophyte,thallus,alternation of generation,marchantia,funaria,selaginella,pinus,cycas,"
 "heterospor,spirogyra,volvox,laminaria,sargassum,fucus,porphyra,gelidium,agar,algin,carrageen,protonema,archegonium,"
 "antheridium,coralloid,prothallus,sphagnum,isogamy,oogamy,haplontic,diplontic,haplo-diplontic,zoospore,pyrenoid,fucoxanthin,"
 "phycoerythrin,equisetum,dryopteris,pteris,ginkgo,cone,strobilus,sporophyll,sorus,rhizoid,gemma,peat,naked seed,vascular cryptogam"),
("morphology-flowering-plants", "Morphology of Flowering Plants", "Biology",
 "morphology of flowering plants,morphology,flower,inflorescence,root morphology",
 "tap root,fibrous root,adventitious,root cap,root hair,region of elongation,pneumatophore,stilt root,prop root,velamen,stem tendril,"
 "phylloclade,cladode,rhizome,tuber,stolon,runner,sucker,offset,bulb,corm,compound leaf,simple leaf,pinnate,palmate,venation,"
 "phyllotaxy,leaf base,pulvinus,leaf tendril,inflorescence,racemose,cymose,aestivation,placentation,valvate,twisted,imbricate,"
 "vexillary,epigynous,perigynous,hypogynous,zygomorphic,actinomorphic,bisexual,unisexual,gynoecium,androecium,syncarpous,"
 "apocarpous,fabaceae,solanaceae,liliaceae,brassicaceae,caryopsis,drupe,berry,pome,hesperidium,legume,perianth,corolla,calyx,"
 "epipetalous,diadelphous,monadelphous,polyadelphous,axile,marginal placentation,parietal,free central,basal,bracts,ovary,"
 "monocotyledonous seed,dicotyledonous seed,scutellum,aleurone,hilum,micropyle,coleoptile,coleorhiza,floral formula,floral diagram"),
("anatomy-flowering-plants", "Anatomy of Flowering Plants", "Biology",
 "anatomy of flowering plants,plant anatomy,tissue,tissue system,secondary growth",
 "meristem,xylem,phloem,cambium,vascular bundle,tissue system,epidermis,stomata,stoma,guard cell,collenchyma,sclerenchyma,"
 "parenchyma,sieve tube,companion cell,tracheid,annual ring,heartwood,sapwood,cork cambium,phellogen,lenticel,secondary growth,"
 "dicot stem,monocot root,monocot stem,dicot root,bulliform,endodermis,casparian,pericycle,conjunctive,pith,medullary,hypodermis,"
 "bast,aerenchyma,periderm,spring wood,autumn wood,intrafascicular,interfascicular,protoxylem,metaxylem,open vascular,"
 "closed vascular,radial vascular,conjoint,phelloderm,sclereid,fibre,trichome,root hair,ground tissue,cortex,subsidiary"),
("structural-organisation-animals", "Structural Organisation in Animals", "Biology",
 "structural organisation in animals,animal tissues,animal tissue,epithelial tissue,cockroach,frog,earthworm",
 "epithelium,epithelial,connective tissue,muscular tissue,neural tissue,squamous,cuboidal,columnar,ciliated epithelium,glandular,"
 "tight junction,adhering junction,gap junction,adipose,cartilage,areolar,cockroach,frog,earthworm,malpighian,pheretima,periplaneta,"
 "rana,tendon,ligament,fibroblast,mast cell,macrophage,collagen,desmosome,tissue,exocrine,endocrine gland,compound epithelium,"
 "simple epithelium,stratified,pseudostratified,transitional,striated,smooth muscle,cardiac muscle,neuroglia,neuron,hepatopancreatic,"
 "typhlosole,clitellum,spermathecae,gizzard,crop,proventriculus,mushroom gland,ootheca,anal cerci,sclerite,tegmina,nephridia,"
 "chloragogen,blood gland,fat body,urecose gland,dense regular,dense irregular,reticular"),
("cell-unit-of-life", "Cell: The Unit of Life", "Biology",
 "cell the unit of life,cell,cell organelles,organelles,cell biology,cell membrane",
 "cell theory,prokaryotic,eukaryotic,mitochondria,mitochondrion,golgi,endoplasmic reticulum,ribosome,lysosome,vacuole,plastid,"
 "chloroplast,nucleus,nucleolus,centrosome,centriole,cilia,flagella,plasma membrane,fluid mosaic,cell wall,microbody,peroxisome,"
 "glyoxysome,chromatin,mesosome,nucleoid,plasmid,cytoskeleton,organelle,schleiden,schwann,virchow,singer,nicolson,porin,"
 "cristae,matrix,thylakoid,grana,stroma,leucoplast,chromoplast,amyloplast,elaioplast,tonoplast,cisternae,sarcoplasmic,"
 "rough er,smooth er,spindle fibre,satellite,nuclear pore,nuclear envelope,cytoplasm,protoplasm,gram positive,cell envelope,"
 "capsule,slime layer,pili,fimbriae,mycoplasma,pplo,lampbrush,polytene,robert hooke,leeuwenhoek,palade"),
("biomolecules", "Biomolecules", "Biology & Chemistry",
 "biomolecules,biomolecule,biomolecules chemistry,enzymes,enzyme,proteins,carbohydrates,lipids,vitamins,amino acids,nucleic acids",
 "amino acid,protein,enzyme,carbohydrate,lipid,nucleic acid,polysaccharide,glycosidic,peptide bond,cofactor,coenzyme,"
 "competitive inhibition,active site,michaelis,vmax,glycogen,starch,cellulose,chitin,fatty acid,phospholipid,triglyceride,"
 "nucleotide,nucleoside,denaturation,zwitterion,primary structure,secondary structure,tertiary,quaternary,isoenzyme,ribozyme,"
 "holoenzyme,apoenzyme,prosthetic,metabolite,lecithin,glycine,alanine,glucose,fructose,sucrose,maltose,lactose,anomer,"
 "mutarotation,vitamin,monosaccharide,disaccharide,oligosaccharide,reducing sugar,invert sugar,fibrous protein,globular protein,"
 "essential amino acid,saturated,unsaturated,oligopeptide,helix,pleated,collagen,insulin,haemoglobin,abzyme,transferase,"
 "oxidoreductase,hydrolase,lyase,isomerase,ligase,optimum temperature,substrate concentration,rubisco,biomacromolecule,"
 "acid soluble pool,lactic acid,glycerol,gum,cellobiose,glycolipid,sphingosine,sugar,ketose,aldose,epimer,osazone,pyranose,furanose,"
 "haworth,amylose,amylopectin,scurvy,rickets,beriberi,night blindness,pernicious,isoelectric,essential amino,fat soluble,water soluble vitamin,enzymatic,transition state,intermediate state,substrate"),
("cell-cycle-division", "Cell Cycle and Cell Division", "Biology",
 "cell cycle and cell division,cell division,mitosis,meiosis,cell cycle",
 "mitosis,meiosis,prophase,metaphase,anaphase,telophase,interphase,cytokinesis,karyokinesis,synaptonemal,crossing over,"
 "chiasmata,bivalent,leptotene,zygotene,pachytene,diplotene,diakinesis,cell cycle,g1 phase,s phase,g2 phase,checkpoint,cdk,"
 "cyclin,spindle,kinetochore,centromere,dyad,tetrad,quiescent,cell plate,phragmoplast,cleavage furrow,equational,reductional,"
 "recombination nodule,chromatid,homologous chromosome,mitotic,meiotic,condensation,g0,sister chromatid,terminalisation"),
("photosynthesis", "Photosynthesis in Higher Plants", "Biology",
 "photosynthesis in higher plants,photosynthesis,light reaction,calvin cycle,c3 c4",
 "photosynthesis,photosynthetic,chlorophyll,light reaction,calvin,c4,c3,kranz,rubisco,photosystem,photophosphorylation,"
 "photorespiration,hatch,slack,pep carboxylase,pepcase,thylakoid,grana,blackman,limiting factor,emerson,engelmann,cam plant,"
 "oxygenase,z scheme,chemiosmotic,nadph,action spectrum,absorption spectrum,carotenoid,xanthophyll,cyclic,non-cyclic,oec,"
 "p680,p700,rubp,pga,reaction centre,light harvesting,chlorophyll a,bundle sheath,mesophyll,priestley,ingenhousz,sachs,"
 "van niel,cornelius,calvin cycle,carboxylation,reduction,regeneration,oxaloacetate,ctp,dark reaction,biosynthetic phase"),
("respiration-plants", "Respiration in Plants", "Biology",
 "respiration in plants,plant respiration,cellular respiration,glycolysis,krebs cycle",
 "glycolysis,krebs,tca,citric acid cycle,oxidative phosphorylation,electron transport,fermentation,anaerobic,respiratory quotient,"
 "pyruvic,pyruvate,acetyl coa,oxaloacetate,atp synthase,cytochrome,fadh2,nadh,substrate level,aerobic respiration,"
 "respiratory substrate,alcoholic fermentation,lactic acid fermentation,amphibolic,respiratory balance sheet,complex i,"
 "complex iv,ubiquinone,f0,f1,fructose 1 6,phosphofructokinase,hexokinase,succinate,fumarate,malate,oxidation of pyruvate,"
 "respiration,respiratory pathway,rq"),
("plant-growth-development", "Plant Growth and Development", "Biology",
 "plant growth and development,plant hormones,plant growth regulators,auxin",
 "auxin,gibberellin,cytokinin,ethylene,abscisic,aba,photoperiod,vernalisation,vernalization,phytochrome,florigen,senescence,"
 "abscission,apical dominance,bolting,growth regulator,plant growth,arithmetic growth,geometric growth,sigmoid,differentiation,"
 "dedifferentiation,redifferentiation,meristematic,short day,long day,day neutral,iaa,2 4 d,iba,naa,kinetin,zeatin,malting,"
 "parthenocarpy,seed dormancy,tropism,phototropism,photoperiodism,growth rate,relative growth,phytohormone,ripening,"
 "stress hormone,gibberella fujikuroi,bakanae,coconut milk,cell elongation,growth phase,lag phase,log phase,"),
("transport-in-plants", "Transport in Plants", "Biology",
 "transport in plants,water transport,translocation,transpiration,osmosis",
 "water potential,osmosis,plasmolysis,imbibition,diffusion,facilitated,aquaporin,symplast,apoplast,transpiration,cohesion,"
 "tension,root pressure,guttation,stomatal,translocation,pressure flow,mass flow,active transport,uniport,symport,antiport,"
 "turgor,wall pressure,solute potential,pressure potential,ascent of sap,potometer,phloem loading,source,sink,bulk flow,"
 "wilting,hypertonic,hypotonic,isotonic,endosmosis,exosmosis,turgid,flaccid,carrier protein,ion channel,porin,"),
("mineral-nutrition", "Mineral Nutrition", "Biology",
 "mineral nutrition,plant nutrition,nitrogen fixation,nitrogen cycle",
 "mineral nutrition,macronutrient,micronutrient,deficiency,chlorosis,necrosis,nitrogen fixation,nitrogenase,nodule,"
 "leghemoglobin,leghaemoglobin,rhizobium,nitrification,denitrification,ammonification,nitrobacter,nitrosomonas,hydroponics,"
 "essential element,toxicity,nitrate reductase,transamination,reductive amination,biological nitrogen,azotobacter,frankia,"
 "hidden hunger,little leaf,whiptail,die back,mottling,nodulation,soilless,amide,ureide,glutamate,glutamine,"),
("digestion-absorption", "Digestion and Absorption", "Biology",
 "digestion and absorption,digestion,digestive system,alimentary canal",
 "digestion,absorption,alimentary,salivary,amylase,pepsin,trypsin,chymotrypsin,lipase,bile,liver,gall bladder,pancreatic juice,"
 "enterokinase,brunner,lieberkuhn,villi,duodenum,jejunum,ileum,colon,caecum,rectum,stomach,oesophagus,peristalsis,"
 "deglutition,chyme,chyle,hcl,intrinsic factor,kwashiorkor,marasmus,jaundice,vomiting,diarrhoea,constipation,indigestion,"
 "dentition,thecodont,heterodont,diphyodont,enamel,dentine,mastication,micelle,chylomicron,glisson,sphincter,rennin,"
 "gastric juice,succus entericus,goblet cell,paneth,emulsification,vermiform,appendix,nutrition,pylorus,cardiac sphincter,"
 "carboxypeptidase,nuclease,dipeptidase,maltase,sucrase,lactase,cholecystokinin,secretin,gastrin,enterogastrone,bilirubin,biliverdin"),
("breathing-gas-exchange", "Breathing and Exchange of Gases", "Biology",
 "breathing and exchange of gases,breathing,respiration human,respiratory system,lungs",
 "breathing,lungs,alveoli,alveolar,pulmonary,vital capacity,tidal volume,residual volume,inspiratory,expiratory,spirometer,"
 "bronchi,bronchiole,diaphragm,oxyhaemoglobin,carbonic anhydrase,bohr,oxygen dissociation,intercostal,pleura,"
 "respiratory rhythm,pneumotaxic,chloride shift,emphysema,asthma,occupational respiratory,partial pressure,trachea,"
 "larynx,epiglottis,glottis,functional residual,total lung capacity,dead space,ventilation,thoracic,respiratory centre,"
 "chemosensitive,hypoxia,silicosis,asbestosis,pneumonia,carbaminohaemoglobin,bicarbonate,respiratory membrane,pco2,po2,"
 "inspiratory reserve,expiratory reserve,breathing rate,gaseous exchange"),
("body-fluids-circulation", "Body Fluids and Circulation", "Biology",
 "body fluids and circulation,blood,heart,circulatory system,circulation",
 "blood,plasma,rbc,erythrocyte,wbc,leucocyte,neutrophil,eosinophil,basophil,lymphocyte,monocyte,platelet,thrombocyte,"
 "coagulation,clotting,fibrinogen,thrombin,heart,atrium,ventricle,cardiac,ecg,qrs,systole,diastole,pulse,blood pressure,"
 "hypertension,coronary,angina,atherosclerosis,lymph,blood group,rh factor,erythroblastosis,sa node,av node,purkinje,"
 "bundle of his,double circulation,open circulatory,closed circulatory,heart sound,stroke volume,cardiac output,tricuspid,"
 "bicuspid,mitral,aorta,vena cava,pulmonary artery,pulmonary vein,heart failure,cardiac arrest,pacemaker,hepatic portal,"
 "rhesus,antigen a,antibody,agglutination,serum,haemoglobin,lymphatic,tissue fluid,thromboplastin,prothrombin,heparin,"
 "diapedesis,cardiac cycle,pericardium,myocardium,endocardium,chordae,semilunar,coronary artery disease"),
("excretory-products", "Excretory Products and their Elimination", "Biology",
 "excretory products and their elimination,excretion,kidney,nephron,urine formation",
 "nephron,kidney,glomerul,bowman,proximal convoluted,henle,distal convoluted,collecting duct,juxtaglomerular,jga,gfr,"
 "ultrafiltration,tubular reabsorption,tubular secretion,urine,ureter,urinary bladder,micturition,adh,vasopressin,renin,"
 "angiotensin,aldosterone,anp,atrial natriuretic,dialysis,haemodialysis,uremia,renal calculi,glomerulonephritis,"
 "ammonotelic,ureotelic,uricotelic,excretion,protonephridia,malpighian tubule,green gland,flame cell,counter current,"
 "vasa recta,podocyte,urea cycle,osmoregulation,cortex,medulla,renal pelvis,calyx,pyramids,filtration slit,"
 "juxta medullary,cortical nephron,urea,uric acid,ammonia,macula densa,diuresis,antidiuretic,nephritis,renal"),
("locomotion-movement", "Locomotion and Movement", "Biology",
 "locomotion and movement,locomotion,muscles,skeletal system,joints,bones",
 "muscle,sarcomere,actin,myosin,troponin,tropomyosin,sliding filament,skeletal system,bone,vertebra,vertebral column,rib,"
 "sternum,skull,cranium,pectoral girdle,pelvic girdle,femur,humerus,joint,synovial,pivot joint,hinge joint,"
 "ball and socket,gliding joint,saddle joint,fibrous joint,cartilaginous joint,osteoporosis,arthritis,gout,myasthenia,"
 "tetany,muscular dystrophy,sarcoplasmic,sarcolemma,z line,a band,i band,h zone,red muscle,white muscle,myoglobin,"
 "motor unit,creatine phosphate,atlas,phalanges,carpals,tarsals,patella,scapula,clavicle,coccyx,sacrum,ulna,radius,tibia,"
 "fibula,amoeboid movement,ciliary movement,muscle fatigue,cross bridge,myofibril,myofilament,thick filament,thin filament,"
 "sacral,lumbar,cervical,thoracic vertebrae,hyoid,sphenoid,ethmoid,mandible,maxilla,floating ribs,acetabulum,glenoid"),
("neural-control-coordination", "Neural Control and Coordination", "Biology",
 "neural control and coordination,nervous system,neuron,brain,sense organs,eye,ear",
 "neuron,axon,dendrite,synapse,neurotransmitter,action potential,resting potential,nerve impulse,myelin,node of ranvier,"
 "cns,pns,brain,cerebrum,cerebellum,medulla oblongata,hypothalamus,thalamus,corpus callosum,reflex arc,sympathetic,"
 "parasympathetic,autonomic,cranial nerve,spinal cord,meninges,retina,rod cell,cone cell,rhodopsin,cornea,lens,iris,"
 "vitreous,aqueous,cochlea,organ of corti,eustachian,tympanic,semicircular,vestibular,ossicle,malleus,incus,stapes,fovea,"
 "blind spot,limbic,amygdala,sensory receptor,olfactory,gustatory,acetylcholine,saltatory,depolarisation,repolarisation,"
 "sodium potassium pump,somatic,afferent,efferent,forebrain,midbrain,hindbrain,pons,sclera,choroid,ciliary body,"
 "pupil,cerebral cortex,grey matter,white matter,basilar membrane,reissner,tectorial,hair cell,photoreceptor,"
 "bipolar neuron,unipolar,multipolar,schwann cell,nissl,dura mater,pia mater,arachnoid"),
("chemical-coordination", "Chemical Coordination and Integration", "Biology",
 "chemical coordination and integration,hormones,endocrine system,endocrine,hormone",
 "hormone,endocrine,pituitary,thyroid,parathyroid,adrenal,pancreas,insulin,glucagon,thymus,pineal,melatonin,gonad,"
 "testosterone,oestrogen,estrogen,progesterone,hcg,relaxin,growth hormone,acromegaly,gigantism,dwarfism,cretinism,goitre,"
 "hyperthyroid,graves,myxoedema,cortisol,adrenaline,epinephrine,noradrenaline,diabetes mellitus,diabetes insipidus,"
 "addison,cushing,conn,tsh,acth,fsh,lh,prolactin,oxytocin,calcitonin,pth,thyroxine,second messenger,camp,"
 "hypothalamic,releasing hormone,melanocyte,islets of langerhans,alpha cell,beta cell,zona glomerulosa,zona fasciculata,"
 "zona reticularis,adenohypophysis,neurohypophysis,tetraiodothyronine,triiodothyronine,thymosin,leptin,erythropoietin,"
 "atrial natriuretic,glucocorticoid,mineralocorticoid,androgen,hormone receptor,steroid hormone,peptide hormone"),
("reproduction-organisms", "Reproduction in Organisms", "Biology",
 "reproduction in organisms,asexual reproduction,vegetative propagation",
 "asexual reproduction,binary fission,budding,fragmentation,gemmules,conidia,vegetative propagation,sexual reproduction,"
 "juvenile phase,reproductive phase,senescent phase,oestrus,monoecious,dioecious,gamete,zygote,syngamy,external fertilisation,"
 "internal fertilisation,parthenogenesis,clone,life span,bamboo,strobilanthes,oviparous,viviparous,ovoviviparous,fission,"
 "regeneration,eichhornia,water hyacinth,planarian,hydra,reproduction,bulbil,leaf buds,bryophyllum,eyes of potato,"
 "isogamete,anisogamete,heterogamete,homothallic,heterothallic,estrous,menstrual cycle,perennial,annual,biennial"),
("sexual-reproduction-flowering-plants", "Sexual Reproduction in Flowering Plants", "Biology",
 "sexual reproduction in flowering plants,pollination,fertilisation in plants,double fertilisation,embryo sac",
 "stamen,anther,microsporangium,pollen,microspore,tapetum,sporogenous,pollination,exine,sporopollenin,intine,generative cell,"
 "vegetative cell,megaspore,megasporangium,ovule,embryo sac,synergid,antipodal,egg apparatus,polar nuclei,double fertilisation,"
 "triple fusion,endosperm,embryo,apomixis,polyembryony,parthenocarpy,cleistogamy,chasmogamy,geitonogamy,xenogamy,autogamy,"
 "self incompatibility,pollen pistil,stigma,style,funicle,chalaza,integument,perisperm,epicotyl,hypocotyl,radicle,plumule,"
 "cotyledon,anemophily,entomophily,hydrophily,ornithophily,pollen tube,bagging,emasculation,artificial hybridisation,"
 "nucellus,testa,tegmen,filiform apparatus,male gametophyte,female gametophyte,monosporic,pollen bank,pollen viability,"
 "microsporogenesis,megasporogenesis,seed,fruit,syngamy,tricellular,bicellular,coconut water,false fruit,pseudocarp,"
 "dormancy,albuminous,non-albuminous,apomictic,hypanthodium"),
("human-reproduction", "Human Reproduction", "Biology",
 "human reproduction,reproductive system,male reproductive system,female reproductive system,menstrual cycle",
 "testis,seminiferous,sertoli,leydig,epididymis,vas deferens,seminal vesicle,prostate,bulbourethral,penis,scrotum,"
 "spermatogenesis,spermiogenesis,spermiation,ovary,fallopian,oviduct,uterus,endometrium,myometrium,perimetrium,cervix,vagina,"
 "hymen,labia,mons pubis,clitoris,oogenesis,follicle,graafian,corpus luteum,ovulation,menstrual,menarche,menopause,"
 "fertilisation,implantation,placenta,gestation,parturition,lactation,colostrum,blastocyst,morula,cleavage,trophoblast,"
 "inner cell mass,gastrulation,embryonic,foetus,fetal ejection,acrosome,capacitation,zona pellucida,cumulus,polar body,"
 "primary oocyte,secondary oocyte,spermatid,spermatocyte,spermatogonia,semen,mammary gland,umbilical,amnion,chorion,"
 "allantois,yolk sac,ampulla,isthmus,infundibulum,fimbriae,lh surge,luteal phase,follicular phase,proliferative phase,"
 "secretory phase,mammary alveoli,sperm,ovum,egg,gonadotropin,pregnancy,weeks of pregnancy,trimester,organ systems are formed"),
("reproductive-health", "Reproductive Health", "Biology",
 "reproductive health,contraception,sexually transmitted,infertility,mtp",
 "contraception,iud,copper t,cu-t,lng,oral contraceptive,condom,cervical cap,tubectomy,vasectomy,mtp,medical termination,"
 "sti,std,gonorrhoea,syphilis,chlamydia,genital herpes,hepatitis b,trichomoniasis,amniocentesis,art,ivf,zift,gift,icsi,"
 "iui,test tube baby,infertility,population explosion,reproductive health,sex education,saheli,lactational amenorrhea,"
 "rhythm method,periodic abstinence,coitus interruptus,emergency contraceptive,embryo transfer,barrier method,"
 "female foeticide,sex ratio,census,reproductive and child health,rch,natural method,hormonal,implants,"
 "multiload,lippes loop,progestogen,pills,i-pill,tubal,surgical method"),
("principles-inheritance-variation", "Principles of Inheritance and Variation", "Biology",
 "principles of inheritance and variation,genetics,mendel,inheritance,linkage",
 "mendel,monohybrid,dihybrid,test cross,back cross,dominance,co-dominance,codominance,incomplete dominance,multiple allelism,"
 "pleiotropy,polygenic,blood group,linkage,recombination,crossing over,sex determination,sex linked,haemophilia,"
 "colour blindness,thalassemia,sickle cell,phenylketonuria,down syndrome,klinefelter,turner,pedigree,chromosomal theory,"
 "autosomal,aneuploidy,polyploidy,law of segregation,law of dominance,independent assortment,punnett,genotype,phenotype,"
 "allele,homozygous,heterozygous,f1,f2,drosophila,morgan,sutton,boveri,xo type,xy type,zw,haplodiploidy,trisomy,monosomy,"
 "genetic disorder,mendelian disorder,epistasis,carrier,gene,genetic,chromosome,pea plant,variation,sickle,"
 "mutation,gamete formation,dosage,allosome,autosome,hybrid,heredity,phenotypic ratio,genotypic ratio,rryy,cross between,test cross ratio"),
("molecular-basis-inheritance", "Molecular Basis of Inheritance", "Biology",
 "molecular basis of inheritance,dna,rna,replication,transcription,translation,genetic code",
 "dna,rna,replication,transcription,translation,genetic code,codon,anticodon,trna,mrna,rrna,okazaki,helicase,primase,"
 "dna polymerase,ligase,lac operon,operon,repressor,inducer,regulator gene,promoter,terminator,exon,intron,splicing,"
 "capping,tailing,hnrna,central dogma,semiconservative,meselson,stahl,hershey,chase,griffith,avery,macleod,mccarty,"
 "transforming principle,histone,nucleosome,chargaff,watson,crick,double helix,nitrogenous base,purine,pyrimidine,"
 "human genome project,hgp,dna fingerprinting,vntr,snp,est,sequence annotation,wobble,start codon,stop codon,"
 "khorana,nirenberg,template strand,coding strand,polycistronic,gene expression,gene regulation,charging of trna,"
 "aminoacylation,peptidyl transferase,genome,polymerase,gene,mutation,frame shift,point mutation,sanger,taylor,"
 "dna packaging,heterochromatin,euchromatin,ribose,deoxyribose,phosphodiester,hydrogen bond,uracil,thymine,"
 "adenine,guanine,cytosine,bacteriophage,rna world,rna polymerase,sigma factor,rho factor,ribosomal"),
("evolution", "Evolution", "Biology",
 "evolution,darwin,origin of life,human evolution,natural selection",
 "evolution,darwin,lamarck,natural selection,hardy weinberg,genetic drift,founder effect,bottleneck,adaptive radiation,"
 "convergent,divergent,homologous organ,analogous organ,vestigial,atavism,fossil,miller,urey,oparin,haldane,abiogenesis,"
 "biogenesis,panspermia,archaeopteryx,dryopithecus,ramapithecus,australopithecus,homo habilis,homo erectus,neanderthal,"
 "cro-magnon,homo sapiens,speciation,industrial melanism,peppered moth,biston,mutation theory,de vries,saltation,"
 "geological time,paleozoic,mesozoic,cenozoic,coelacanth,stabilising selection,directional selection,disruptive selection,"
 "evolutionary,origin of life,galapagos,finches,malthus,gene flow,genetic equilibrium,allopatric,sympatric,"
 "embryological,comparative anatomy,biochemical similarities,stromatolite,cambrian,ordovician,devonian,carboniferous,"
 "permian,triassic,jurassic,cretaceous,tertiary,quaternary,age of reptiles,age of fishes,dinosaur,brain capacity,"
 "fitness,survival of the fittest,wallace,mimicry,coacervate,microsphere,protobiont,primitive atmosphere"),
("human-health-disease", "Human Health and Disease", "Biology",
 "human health and disease,diseases,immunity,immune system,cancer,aids,drugs,vaccination",
 "immunity,antibody,antigen,vaccine,vaccination,innate,acquired,humoral,cell mediated,t cell,b cell,interferon,"
 "immunoglobulin,igg,iga,igm,ige,igd,allergy,autoimmune,rheumatoid,hiv,aids,cancer,carcinogen,oncogene,metastasis,benign,"
 "malignant,tumour,biopsy,pathogen,typhoid,pneumonia,malaria,plasmodium,amoebiasis,ascariasis,filariasis,elephantiasis,"
 "ringworm,dengue,chikungunya,common cold,rhinovirus,widal,elisa,drug,opioid,morphine,heroin,cannabinoid,cocaine,"
 "amphetamine,barbiturate,alcohol,tobacco,nicotine,adolescence,addiction,tetanus,dpt,bcg,passive immunity,active immunity,"
 "anaphylaxis,mast cell,histamine,lymphoid,thymus,bone marrow,mhc,graft rejection,transplantation,salmonella,haemophilus,"
 "wuchereria,entamoeba,trichophyton,microsporum,epidermophyton,anopheles,aedes,gametocyte,sporozoite,haemozoin,"
 "reverse transcriptase,provirus,helper t,cytotoxic,memory cell,primary response,secondary response,withdrawal,"
 "cannabis,marijuana,hashish,charas,ganja,coca,datura,atropa,papaver,health,disease,infection,viral,bacterial"),
("microbes-human-welfare", "Microbes in Human Welfare", "Biology",
 "microbes in human welfare,microbes,biogas,sewage treatment,fermentation industrial",
 "lactic acid bacteria,curd,yeast,bread,idli,dosa,toddy,cheese,swiss cheese,roquefort,propionibacterium,fermented,"
 "fermentor,streptokinase,cyclosporin,statin,monascus,lipase,pectinase,protease,sewage,primary treatment,secondary treatment,"
 "activated sludge,flocs,bod,biogas,methanogen,methanobacterium,gobar gas,biocontrol,bacillus thuringiensis,trichoderma,"
 "baculovirus,nucpv,biofertiliser,biofertilizer,anabaena,nostoc,azospirillum,antibiotic,penicillin,fleming,florey,citric acid,"
 "aspergillus niger,acetobacter,clostridium butylicum,butyric acid,lactobacillus,saccharomyces,microbe,effluent,"
 "single cell protein,scp,spirulina,industrial product,bioactive molecule,clarifying agent,ladybird,dragonfly,"
 "blood cholesterol lowering,organic acid,vinegar,wine,beer,whisky,brandy,rum,distilled,fermented beverage"),
("biotechnology-principles", "Biotechnology: Principles and Processes", "Biology",
 "biotechnology principles and processes,biotechnology,recombinant dna technology,genetic engineering,pcr,restriction enzyme",
 "recombinant dna,restriction enzyme,restriction endonuclease,ecori,hindiii,palindromic,sticky ends,blunt ends,plasmid,"
 "pbr322,ori,selectable marker,ampr,tetr,cloning site,bamhi,pvui,insertional inactivation,alpha galactosidase,blue white,"
 "agrobacterium,ti plasmid,gene gun,biolistic,microinjection,competent cell,gel electrophoresis,agarose,ethidium bromide,"
 "pcr,taq polymerase,thermus aquaticus,bioreactor,stirred tank,sparged,downstream processing,ligation,elution,annealing,"
 "extension,cloning vector,expression vector,host cell,rop,transformation,calcium chloride,reporter,genetic engineering,biotechnology,"
 "exonuclease,endonuclease,boyer,cohen,gene cloning,amplification,primers,thermostable,sparger,probe"),
("biotechnology-applications", "Biotechnology and its Applications", "Biology",
 "biotechnology and its applications,transgenic,gm crops,gene therapy,bt cotton,biopiracy",
 "bt toxin,bt cotton,cry,pest resistant,transgenic,gm crop,genetically modified,golden rice,rna interference,rnai,"
 "nematode,meloidogyne,humulin,eli lilly,pro-insulin,proinsulin,c peptide,gene therapy,ada deficiency,adenosine deaminase,"
 "molecular diagnosis,autoradiography,biopiracy,patent,basmati,rosie,alpha-1 antitrypsin,transgenic animal,bioethics,geac,"
 "flavr savr,herbicide,bt brinjal,biosafety,transgene,biopatent,pest,cry protein,insecticidal,stunted,gene silencing,"
 "ssrna,dsrna,cecropia,bacillus thuringiensis,crylab,cryiiab,cryiab,vitamin a enriched,protein enriched,recombinant therapeutics,therapeutics,approved worldwide"),
("organisms-and-populations", "Organisms and Populations", "Biology",
 "organisms and populations,ecology,population,population interactions,adaptations",
 "population,natality,mortality,immigration,emigration,age pyramid,logistic growth,exponential growth,carrying capacity,"
 "verhulst,r selected,k selected,life history,population interaction,mutualism,commensalism,parasitism,predation,"
 "competition,amensalism,gause,competitive exclusion,resource partitioning,brood parasitism,cuckoo,adaptation,allen,"
 "bergmann,thermoregulat,osmoregulat,hibernation,diapause,migration,kangaroo rat,habitat,niche,biome,abiotic factor,"
 "ecotype,euryhaline,stenohaline,eurythermal,stenothermal,lotka,volterra,intrinsic rate,biotic potential,population density,"
 "ecology,organism,acacia,calotropis,ophrys,orchid,cattle egret,barnacle,clown fish,sea anemone,lichen,mycorrhiza,"
 "ectoparasite,endoparasite,cuscuta,aestivation,xerophytic,ecological,tolerance,regulate,conform,suspend,"),
("ecosystem", "Ecosystem", "Biology",
 "ecosystem,food chain,ecological pyramid,energy flow,ecological succession,nutrient cycling",
 "ecosystem,food chain,food web,trophic level,producer,consumer,decomposer,detritus,grazing food chain,gfc,dfc,energy flow,"
 "ecological pyramid,pyramid of,productivity,gpp,npp,primary production,10 percent law,ten percent,succession,pioneer species,"
 "climax,hydrarch,xerarch,sere,nutrient cycling,carbon cycle,phosphorus cycle,sedimentary cycle,gaseous cycle,humification,"
 "mineralisation,leaching,catabolism,fragmentation,ecosystem services,costanza,standing crop,standing state,lindeman,"
 "biomass,hydrosere,lithosere,seral,litter,detritivore,humus,trophic,secondary productivity,photosynthetically active,"
 "par,inverted pyramid,upright pyramid,herbivore,carnivore,omnivore"),
("biodiversity-conservation", "Biodiversity and Conservation", "Biology",
 "biodiversity and conservation,biodiversity,conservation,hotspots,extinction",
 "biodiversity,alpha diversity,beta diversity,gamma diversity,species richness,species area,hotspot,endemism,endemic,"
 "extinction,iucn,red list,in situ,ex situ,national park,sanctuary,biosphere reserve,sacred grove,cryopreservation,seed bank,"
 "zoo,evil quartet,habitat loss,over exploitation,alien species,co-extinction,nile perch,steller,dodo,quagga,thylacine,"
 "earth summit,rio,cbd,johannesburg,amazon,rivet popper,latitudinal gradient,ecosystem diversity,genetic diversity,"
 "species diversity,endangered,vulnerable,critically,western ghats,himalaya,indo-burma,conservation,threatened,"
 "invasive,lantana,parthenium,water hyacinth,african catfish,clarias gariepinus,species number,,bird species,number of species,species are found,highest number"),
("environmental-issues", "Environmental Issues", "Biology",
 "environmental issues,pollution,global warming,ozone,greenhouse effect",
 "pollution,greenhouse,ozone,cfc,global warming,eutrophication,algal bloom,biomagnification,ddt,electrostatic precipitator,"
 "scrubber,catalytic converter,bharat stage,cng,noise pollution,thermal pollution,radioactive,nuclear waste,landfill,e-waste,"
 "solid waste,integrated waste,deforestation,jhum,chipko,reforestation,montreal protocol,kyoto,acid rain,smog,"
 "water pollution,pollutant,chernobyl,arsenic,cultural eutrophication,environmental issues,particulate,decibel,db,"
 "sewage,effluent,toxic,recycling,waste,mining,agrochemical,pcb,herbicide,ultraviolet,uv-b,snow blindness,"),
# --------------------------------------------------------------- ANIMAL KINGDOM
("animal-kingdom", "Animal Kingdom", "Biology",
 "animal kingdom,animalia,phylum,non chordata,chordata,invertebrates,vertebrates,animal classification,jantu jagat",
 "animal kingdom,animalia,basis of classification,porifera,cnidaria,coelenterata,ctenophora,platyhelminthes,aschelminthes,"
 "nematoda,annelida,arthropoda,mollusca,echinodermata,hemichordata,chordata,urochordata,cephalochordata,vertebrata,"
 "cyclostomata,chondrichthyes,osteichthyes,pisces,amphibia,reptilia,aves,mammalia,protochordata,gnathostomata,agnatha,"
 "tunicata,amphioxus,branchiostoma,balanoglossus,asymmetrical,radial symmetry,bilateral symmetry,diploblastic,triploblastic,"
 "coelom,pseudocoel,acoelomate,metamerism,segmentation,notochord,spongocoel,choanocyte,spicule,osculum,canal system,"
 "cnidoblast,nematocyst,polyp,medusa,comb plate,tapeworm,liver fluke,taenia,fasciola,ascaris,wuchereria,nereis,hirudinaria,"
 "leech,apis,bombyx,locusta,limulus,king crab,pila,unio,octopus,sepia,loligo,pinctada,aplysia,chaetopleura,dentalium,"
 "radula,water vascular,aristotle lantern,asterias,echinus,ophiura,antedon,cucumaria,holothuria,scoliodon,torpedo,pristis,"
 "trygon,labeo,catla,clarias,exocoetus,hippocampus,pterophyllum,betta,icthyophis,bufo,hyla,salamandra,chelone,trionyx,"
 "testudo,chameleon,calotes,crocodilus,alligator,hemidactylus,phrynosoma,naja,bangarus,vipera,corvus,columba,psittacula,"
 "struthio,pavo,aptenodytes,neophron,ornithorhynchus,macropus,pteropus,camelus,macaca,rattus,canis,felis,elephas,equus,"
 "delphinus,balaenoptera,panthera,cloaca,air bladder,swim bladder,operculum,lateral line,placoid,cycloid,ctenoid,ganoid,"
 "mantle,visceral hump,trochophore,parapodia,coxal glands,book lungs,spiracle,tracheal,statocyst,bioluminescence,phylum,"
 "subphylum,invertebrate,vertebrate,hermaphrodite,cartilaginous,bony fish,jawless,sea anemone,jellyfish,sponge,physalia,"
 "adamsia,pennatula,gorgonia,meandrina,euspongia,spongilla,sycon,pleurobrachia,ctenoplana,planaria,wuchereria,ancylostoma,"
 "enterobius,dracunculus,trypanosoma,pheretima,neanthes,aphrodite,butterfly,silkworm,honey bee,lac insect,scorpion,spider,"
 "crab,prawn,millipede,centipede,sea urchin,starfish,brittle star,sea lily,sea cucumber,snail,oyster,devil fish,cuttlefish,"
 "mammary glands,feathers,hair,digit,pinna,warm blooded,cold blooded,poikilothermous,homeothermous,viviparous,oviparous,"
 "ovoviviparous,external fertilisation,internal fertilisation,dorsal hollow nerve,pharyngeal gill slits,post anal tail"),
# ---------------------------------------------------------------- PHYSICS
("units-measurements", "Units and Measurements", "Physics",
 "units and measurements,units,dimensions,dimensional analysis,significant figures,errors",
 "dimension,dimensional,si unit,significant figure,least count,vernier,screw gauge,error,percentage error,absolute error,"
 "relative error,fundamental unit,derived unit,planck,light year,parsec,angstrom,order of magnitude,accuracy,precision,"
 "plank's constant,dimensional formula,mlt,physical quantity,unit of,dimensionless,micrometer,rounding"),
("motion-straight-line", "Motion in a Straight Line", "Physics",
 "motion in a straight line,kinematics,1d motion,equations of motion",
 "displacement,velocity,acceleration,uniform acceleration,free fall,retardation,straight line,x t graph,v t graph,"
 "average velocity,instantaneous,relative velocity,kinematic,stopping distance,reaction time,falls from,dropped,thrown vertically,"
 "equation of motion,position time,velocity time,uniformly accelerated,distance covered"),
("motion-plane", "Motion in a Plane", "Physics",
 "motion in a plane,projectile motion,vectors,circular motion,relative motion",
 "projectile,vector,scalar,resultant,unit vector,dot product,cross product,scalar product,vector product,range,maximum height,"
 "time of flight,angle of projection,uniform circular,centripetal,angular velocity,angular speed,horizontal range,"
 "component,resolution,triangle law,parallelogram law,river,boat,swimmer,rain,drift,trajectory,oblique"),
("laws-of-motion", "Laws of Motion", "Physics",
 "laws of motion,newton laws,friction,newtons laws,force",
 "newton,inertia,momentum,impulse,friction,static friction,kinetic friction,limiting friction,coefficient of friction,"
 "banking,pseudo force,free body,tension,pulley,lift,apparent weight,recoil,rocket,equilibrium of,concurrent forces,"
 "angle of repose,block,inclined plane,normal reaction,conservation of momentum,collision,law of motion,string,wedge,weighing machine,conveyor,horizontal force,rough surface,block of mass,body of mass,constant force"),
("work-energy-power", "Work, Energy and Power", "Physics",
 "work energy and power,work energy theorem,kinetic energy,potential energy,power,collision",
 "work done,kinetic energy,potential energy,work energy theorem,conservative,non conservative,power,watt,spring constant,"
 "elastic collision,inelastic collision,coefficient of restitution,efficiency,horse power,mechanical energy,spring,"
 "conservation of energy,vertical circle,loop,work by,energy stored"),
("rotational-motion", "System of Particles and Rotational Motion", "Physics",
 "system of particles and rotational motion,rotational motion,moment of inertia,torque,angular momentum,centre of mass",
 "centre of mass,center of mass,moment of inertia,torque,angular momentum,radius of gyration,rolling,pure rolling,"
 "parallel axis,perpendicular axis,rotational kinetic,angular acceleration,couple,equilibrium of rigid,disc,ring,sphere,"
 "solid cylinder,hollow,rod,rigid body,angular impulse,precession,slipping,flywheel,lever,balance,"),
("gravitation", "Gravitation", "Physics",
 "gravitation,gravity,kepler,satellite,escape velocity",
 "gravitation,gravitational,kepler,satellite,orbital velocity,escape velocity,acceleration due to gravity,g at depth,"
 "geostationary,universal gravitational,gravitational potential,gravitational field,binding energy,orbital period,"
 "weightlessness,planet,earth's surface,polar,equator,height h above,altitude,moon,time period of satellite"),
("mechanical-properties-solids", "Mechanical Properties of Solids", "Physics",
 "mechanical properties of solids,elasticity,youngs modulus,stress strain",
 "stress,strain,young's modulus,youngs modulus,bulk modulus,modulus of rigidity,shear modulus,poisson,hooke,elastic limit,"
 "elastic potential energy,breaking stress,elasticity,wire is stretched,elongation,longitudinal strain,tensile,"
 "yield point,ductile,brittle,elastomer,work done in stretching"),
("mechanical-properties-fluids", "Mechanical Properties of Fluids", "Physics",
 "mechanical properties of fluids,fluid mechanics,surface tension,viscosity,bernoulli,pressure",
 "pressure,pascal,archimedes,buoyancy,bernoulli,streamline,viscosity,stokes,terminal velocity,reynolds,surface tension,"
 "capillary,capillarity,angle of contact,excess pressure,soap bubble,droplet,hydraulic,manometer,barometer,atmospheric pressure,"
 "equation of continuity,venturi,torricelli,efflux,floating,density,upthrust,laminar,turbulent,meniscus,coefficient of viscosity,"
 "gauge pressure,absolute pressure,fluid,liquid column,flow rate,stars,"),
("thermal-properties-matter", "Thermal Properties of Matter", "Physics",
 "thermal properties of matter,heat,calorimetry,thermal expansion,conduction,radiation",
 "thermal expansion,coefficient of linear,coefficient of volume,specific heat,latent heat,calorimetry,conduction,convection,"
 "radiation,stefan,boltzmann,newton's law of cooling,wien,black body,thermal conductivity,thermal resistance,heat capacity,"
 "melting,boiling point,calorimeter,emissivity,temperature scale,celsius,fahrenheit,kelvin,steady state,ice,steam,"
 "heat transfer,water equivalent,absorptive power,emissive power,final temperature,temperature of the mixture,ice at,water at,mixed with,rooms at,bodies a b c"),
("thermodynamics", "Thermodynamics", "Physics",
 "thermodynamics physics,laws of thermodynamics,carnot,heat engine",
 "thermodynamic,first law,second law,isothermal,adiabatic,isobaric,isochoric,carnot,heat engine,refrigerator,coefficient of performance,"
 "internal energy,cyclic process,p v diagram,pv diagram,work done by gas,efficiency of engine,entropy,reversible,irreversible,"
 "zeroth law,thermal equilibrium,quasi static,free expansion,cp,cv,molar specific heat,sink,source,thermodynamics"),
("kinetic-theory", "Kinetic Theory", "Physics",
 "kinetic theory,kinetic theory of gases,ideal gas,rms speed,degrees of freedom",
 "kinetic theory,ideal gas,rms speed,root mean square,mean free path,degrees of freedom,equipartition,avogadro,boltzmann constant,"
 "gas equation,pv = nrt,molar mass,ideal gas equation,most probable speed,average speed,monatomic,diatomic,polyatomic,"
 "gas molecules,collision of molecules,real gas,vander waals,mixture of gases,dalton,"),
("oscillations", "Oscillations", "Physics",
 "oscillations,shm,simple harmonic motion,pendulum,spring",
 "simple harmonic,shm,oscillation,oscillator,time period,frequency,amplitude,phase,pendulum,spring mass,spring constant,"
 "damped,forced oscillation,resonance,restoring force,angular frequency,displacement of particle,maximum acceleration,"
 "maximum velocity,equation of motion of particle,periodic,second's pendulum,simple pendulum,physical pendulum,"
 "torsional,combination of springs,series spring,parallel spring"),
("waves", "Waves", "Physics",
 "waves,sound waves,wave motion,doppler effect,standing waves,beats",
 "wave,transverse,longitudinal,wavelength,speed of sound,doppler,beats,standing wave,stationary wave,node,antinode,"
 "organ pipe,closed pipe,open pipe,harmonic,overtone,fundamental frequency,string fixed,sonometer,resonance tube,"
 "kundt,progressive wave,wave equation,intensity of sound,decibel,superposition,interference of sound,reflection of wave,"
 "vibrating string,tuning fork,sound"),
("electric-charges-fields", "Electric Charges and Fields", "Physics",
 "electric charges and fields,electrostatics,coulomb law,gauss law,electric field,electric dipole",
 "coulomb,electric field,field lines,gauss,flux,dipole,dipole moment,charge,quantisation,conservation of charge,induction,"
 "conductor,insulator,uniform charge,infinite sheet,line charge,ring of charge,spherical shell,point charge,torque on dipole,"
 "electric flux,permittivity,test charge,net force on charge,charged sphere,electrostatic force,charged particle in field"),
("electrostatic-potential-capacitance", "Electrostatic Potential and Capacitance", "Physics",
 "electrostatic potential and capacitance,capacitor,potential,capacitance,dielectric",
 "potential,potential difference,equipotential,capacitor,capacitance,dielectric,series combination,parallel combination,"
 "energy stored,farad,parallel plate,spherical capacitor,cylindrical,dielectric constant,polarisation,potential energy of dipole,"
 "work done in moving charge,potential due to,common potential,redistribution,battery connected,plates,electric potential"),
("current-electricity", "Current Electricity", "Physics",
 "current electricity,ohm law,kirchhoff,resistance,wheatstone,potentiometer",
 "electric current,resistance,resistivity,conductivity,ohm,drift velocity,mobility,kirchhoff,wheatstone,meter bridge,potentiometer,"
 "emf,internal resistance,terminal voltage,galvanometer shunt,ammeter,voltmeter,joule heating,power dissipated,"
 "colour code,temperature coefficient,battery,electric circuit,electrical energy,fuse,resistor,rheostat,balanced bridge,"
 "null point,ohmic,electric current,relaxation time,bulb,ohm's law,voltmeter of resistance"),
("moving-charges-magnetism", "Moving Charges and Magnetism", "Physics",
 "moving charges and magnetism,magnetic effect of current,biot savart,ampere,lorentz force,cyclotron",
 "magnetic field,biot,savart,ampere,solenoid,toroid,lorentz,cyclotron,moving coil,galvanometer,force on current carrying,"
 "magnetic moment of loop,torque on loop,helical path,velocity selector,straight wire,circular loop,parallel wires,"
 "circular coil,radius of path,mass spectrometer,magnetic force,right hand,left hand,flux density,oersted,current sensitivity"),
("magnetism-matter", "Magnetism and Matter", "Physics",
 "magnetism and matter,magnet,earth magnetism,bar magnet,paramagnetic,diamagnetic,ferromagnetic",
 "bar magnet,magnetic dipole,magnetic moment,earth's magnetic,declination,dip,inclination,horizontal component,paramagnetic,"
 "diamagnetic,ferromagnetic,susceptibility,permeability,hysteresis,coercivity,retentivity,curie,neutral point,magnetic poles,"
 "magnetic field lines,gauss law for magnetism,electromagnet,soft iron,steel,magnetisation,intensity of magnetisation,"
 "short bar magnet,magnetic meridian,potential energy of magnet"),
("electromagnetic-induction", "Electromagnetic Induction", "Physics",
 "electromagnetic induction,emi,faraday,lenz,self inductance,mutual inductance,eddy current",
 "faraday,lenz,induced emf,induced current,magnetic flux,self inductance,mutual inductance,inductor,eddy current,motional emf,"
 "generator,rate of change of flux,henry,coil rotating,rod moving,conducting rod,loop in magnetic field,transformer"),
("alternating-current", "Alternating Current", "Physics",
 "alternating current,ac,lcr circuit,transformer,resonance",
 "alternating,rms value,peak value,impedance,reactance,inductive reactance,capacitive reactance,lcr,series lcr,resonance,quality factor,"
 "power factor,wattless,transformer,step up,step down,ac generator,phasor,choke,average power,ac source,ac voltage,"
 "ac circuit,lc oscillation,hot wire ammeter,rms current,phase difference between"),
("electromagnetic-waves", "Electromagnetic Waves", "Physics",
 "electromagnetic waves,em waves,displacement current,electromagnetic spectrum",
 "electromagnetic wave,displacement current,maxwell,electromagnetic spectrum,gamma rays,x-rays,x rays,ultraviolet,infrared,"
 "microwave,radio wave,visible light,speed of light in vacuum,e and b,amplitude of electric field,poynting,"
 "radiation pressure,intensity of em,transverse nature,greenhouse,ozone layer absorbs,wavelength of em"),
("ray-optics", "Ray Optics and Optical Instruments", "Physics",
 "ray optics and optical instruments,ray optics,reflection,refraction,lens,mirror,prism,microscope,telescope",
 "mirror,lens,focal length,refraction,reflection,refractive index,total internal reflection,critical angle,prism,"
 "angle of deviation,minimum deviation,dispersion,rainbow,microscope,telescope,magnifying power,power of lens,"
 "lens maker,concave,convex,real image,virtual image,magnification,optical fibre,mirage,apparent depth,"
 "eye defects,myopia,hypermetropia,presbyopia,astigmatism,objective,eyepiece,thin lens,combination of lenses,"
 "plane mirror,spherical mirror,newton's formula,normal shift,glass slab,silvered,aberration,scattering"),
("wave-optics", "Wave Optics", "Physics",
 "wave optics,interference,diffraction,polarisation,young double slit",
 "interference,diffraction,polarisation,polarization,young's double slit,double slit,fringe width,fringe,coherent,huygens,"
 "wavefront,brewster,malus,polaroid,single slit,central maximum,resolving power,path difference,constructive,destructive,"
 "intensity ratio,phase difference,monochromatic,slit separation,screen distance,thin film,fresnel,fraunhofer,unpolarised,"
 "plane polarised"),
("dual-nature", "Dual Nature of Radiation and Matter", "Physics",
 "dual nature of radiation and matter,photoelectric effect,de broglie,work function,photon",
 "photoelectric,work function,threshold frequency,stopping potential,einstein,photon,de broglie,davisson,germer,matter wave,"
 "kinetic energy of photoelectron,saturation current,cathode ray,electron emission,wave particle,momentum of photon,"
 "intensity of light,photocell,planck's constant,electron volt,thermionic,field emission,hertz,lenard,millikan,"
 "de-broglie wavelength,accelerated through,potential v"),
("atoms", "Atoms", "Physics",
 "atoms,bohr model,hydrogen spectrum,rutherford,atomic structure physics",
 "bohr,hydrogen atom,rutherford,alpha particle scattering,impact parameter,distance of closest approach,energy level,"
 "lyman,balmer,paschen,brackett,pfund,spectral series,rydberg,ionisation energy,excitation,radius of orbit,orbital speed,"
 "quantum number,transition,emission spectrum,absorption spectrum,hydrogen like,he+,li2+,angular momentum quantisation,"
 "ground state,first excited,wavelength of photon emitted,series limit"),
("nuclei", "Nuclei", "Physics",
 "nuclei,nuclear physics,radioactivity,half life,binding energy,fission,fusion",
 "nucleus,nuclear,radioactive,radioactivity,half life,half-life,decay constant,activity,becquerel,curie,mean life,"
 "binding energy,mass defect,fission,fusion,chain reaction,alpha decay,beta decay,gamma decay,isotope,isobar,isotone,"
 "nuclear radius,nuclear density,neutron,proton,mass number,atomic mass unit,amu,q value,reactor,moderator,"
 "control rod,neutrino,positron,disintegration,parent,daughter,radioactive series,nucleon,"),
("semiconductor-electronics", "Semiconductor Electronics", "Physics",
 "semiconductor electronics,semiconductor,diode,transistor,logic gates",
 "semiconductor,diode,p-n junction,pn junction,transistor,logic gate,and gate,or gate,nand,nor,not gate,xor,rectifier,"
 "zener,led,photodiode,solar cell,forward bias,reverse bias,depletion,barrier potential,n-type,p-type,doping,intrinsic,"
 "extrinsic,band gap,valence band,conduction band,common emitter,amplifier,dynamic resistance,current gain,truth table,"
 "boolean,germanium,silicon,donor,acceptor,hole,majority carrier,knee voltage,breakdown,oscillator,"),
# --------------------------------------------------------------- CHEMISTRY
("basic-concepts-chemistry", "Some Basic Concepts of Chemistry", "Chemistry",
 "some basic concepts of chemistry,mole concept,stoichiometry,basic concepts",
 "mole,molar mass,avogadro,stoichiometry,limiting reagent,empirical formula,molecular formula,percentage composition,"
 "molarity,molality,mole fraction,normality,law of conservation of mass,law of definite proportion,multiple proportion,"
 "gay lussac,atomic mass,molecular mass,equivalent weight,significant figures,concentration of solution,mass percent,"
 "dilution,gram equivalent,volume of gas at stp,number of atoms,number of molecules,yield"),
("structure-of-atom", "Structure of Atom", "Chemistry",
 "structure of atom,atomic structure,quantum numbers,orbitals,bohr model chemistry",
 "orbital,quantum number,aufbau,pauli,hund,electronic configuration,shell,subshell,photoelectric,de broglie,heisenberg,"
 "uncertainty,schrodinger,bohr,hydrogen spectrum,wavenumber,rydberg,nodes,radial node,angular node,spin,magnetic quantum,"
 "azimuthal,principal quantum,effective nuclear charge,isoelectronic,thomson,rutherford,chadwick,neutron,electromagnetic radiation,"
 "planck,wave number,atomic orbital,shielding,penetration,exchange energy"),
("periodic-classification", "Classification of Elements and Periodicity in Properties", "Chemistry",
 "classification of elements and periodicity in properties,periodic table,periodicity,ionisation enthalpy,electronegativity",
 "periodic table,periodicity,ionisation enthalpy,ionization enthalpy,electron gain enthalpy,electronegativity,atomic radius,"
 "ionic radius,isoelectronic,diagonal relationship,mendeleev,moseley,modern periodic law,block,period,group,representative,"
 "transition element,inner transition,noble gas,halogen,alkali metal,alkaline earth,metalloid,oxidation state,valency,"
 "screening,lanthanoid contraction,iupac nomenclature of elements,atomic number 100,z > 100"),
("chemical-bonding", "Chemical Bonding and Molecular Structure", "Chemistry",
 "chemical bonding and molecular structure,chemical bonding,vsepr,hybridisation,molecular orbital theory,hydrogen bonding",
 "bond,covalent,ionic bond,vsepr,hybridisation,hybridization,sp3,sp2,sp3d,molecular orbital,bond order,paramagnetic,diamagnetic,"
 "dipole moment,polar,hydrogen bond,lone pair,resonance,formal charge,octet,fajan,bond angle,bond length,bond energy,"
 "sigma bond,pi bond,lattice enthalpy,geometry,shape of molecule,co-ordinate,dative,electrovalent,bonding,antibonding,"
 "intermolecular,london,dispersion,dipole-dipole,ion-dipole,square planar,octahedral,trigonal,tetrahedral,pyramidal,bent,linear"),
("thermodynamics-chem", "Thermodynamics (Chemistry)", "Chemistry",
 "chemical thermodynamics,enthalpy,entropy,gibbs energy,hess law",
 "enthalpy,entropy,gibbs,hess,spontaneous,internal energy,heat of formation,heat of combustion,standard enthalpy,bond enthalpy,"
 "calorimeter,delta h,delta g,delta s,exothermic,endothermic,state function,extensive,intensive,isothermal reversible,"
 "work done in expansion,first law,lattice enthalpy,born haber,enthalpy of neutralisation,enthalpy of solution,"
 "enthalpy of atomisation,sublimation,fusion,vaporisation,second law,third law"),
("equilibrium", "Equilibrium", "Chemistry",
 "equilibrium,chemical equilibrium,ionic equilibrium,le chatelier,ph,buffer",
 "equilibrium,le chatelier,kc,kp,reaction quotient,degree of dissociation,ph,poh,buffer,common ion,solubility product,ksp,"
 "ionic product,acid base,conjugate,lewis acid,bronsted,ka,kb,pka,hydrolysis,salt hydrolysis,henderson,buffer capacity,"
 "dissociation constant,degree of ionisation,haber,backward,forward reaction,equilibrium constant,solubility,precipitation,"
 "indicator,strong acid,weak acid,ostwald dilution"),
("redox-reactions", "Redox Reactions", "Chemistry",
 "redox reactions,oxidation reduction,oxidation number,balancing redox",
 "oxidation,reduction,redox,oxidation number,oxidation state,oxidising agent,reducing agent,disproportionation,"
 "comproportionation,half reaction,ion electron method,balancing,electrode potential,electrochemical series,displacement reaction,"
 "oxidant,reductant,peroxide,superoxide,fractional oxidation"),
("organic-basic-principles", "Organic Chemistry: Some Basic Principles and Techniques", "Chemistry",
 "organic chemistry some basic principles and techniques,goc,general organic chemistry,iupac nomenclature,isomerism,inductive effect",
 "iupac,nomenclature,isomerism,structural isomer,functional isomer,chain isomer,position isomer,metamer,tautomer,optical isomer,"
 "geometrical isomer,chiral,enantiomer,diastereomer,racemic,inductive effect,resonance effect,mesomeric,hyperconjugation,"
 "electromeric,carbocation,carbanion,free radical,nucleophile,electrophile,homolytic,heterolytic,sp3 hybrid carbon,"
 "chromatography,distillation,crystallisation,lassaigne,kjeldahl,dumas,carius,sublimation,steam distillation,"
 "stability of carbocation,acidic strength,basic strength,r s configuration,cis trans,e z,newman,sawhorse,fischer,"
 "functional group,homologous series,degree of unsaturation,dbe,aromatic,aliphatic,alicyclic,nitrogen estimation,iupac name,stereoisomer,cyclic isomer,isomers,how many isomers,major product,hydrocarbon,combustion"),
("hydrocarbons", "Hydrocarbons", "Chemistry",
 "hydrocarbons,alkanes,alkenes,alkynes,benzene,aromatic hydrocarbons",
 "alkane,alkene,alkyne,benzene,aromatic,aromaticity,huckel,wurtz,kolbe,markovnikov,anti markovnikov,peroxide effect,"
 "ozonolysis,hydroboration,hydrogenation,friedel crafts,nitration,sulphonation,halogenation,electrophilic substitution,"
 "conformation,staggered,eclipsed,cracking,pyrolysis,sabatier,lindlar,birch,dehydrohalogenation,saytzeff,addition reaction,"
 "free radical substitution,acetylene,ethyne,ethene,ethane,methane,propene,toluene,naphthalene,cyclohexane,"
 "directing group,ortho para,meta directing,reimer,but 1 yne,hydration of,alkynes,c5h10,butanal,butanone"),
("solutions", "Solutions", "Chemistry",
 "solutions,colligative properties,raoult law,osmotic pressure",
 "solution,colligative,raoult,vapour pressure,osmotic pressure,elevation of boiling,depression of freezing,ebullioscopic,"
 "cryoscopic,van't hoff factor,abnormal molar mass,azeotrope,ideal solution,non ideal,henry's law,molality,mole fraction,"
 "relative lowering,isotonic,hypertonic,reverse osmosis,association,dissociation of solute,solubility of gas,positive deviation,"
 "negative deviation,kb,kf,solute,solvent,boiling point of solution,freezing point of solution"),
("electrochemistry", "Electrochemistry", "Chemistry",
 "electrochemistry,galvanic cell,electrolysis,nernst equation,conductance,kohlrausch",
 "electrochemical cell,galvanic,daniell,electrolysis,faraday,nernst,emf of cell,standard electrode potential,conductance,"
 "molar conductivity,kohlrausch,specific conductance,cell constant,salt bridge,anode,cathode,electrolyte,lead storage battery,"
 "fuel cell,dry cell,mercury cell,corrosion,rusting,limiting molar conductivity,equivalent conductivity,"
 "electrode,half cell,reduction potential,cell potential,gibbs energy and emf,equilibrium constant and emf,"
 "coulomb,deposited,electrolytic,discharge,batteries,ohm-1,e cell,ecell,nernst,n electrons"),
("chemical-kinetics", "Chemical Kinetics", "Chemistry",
 "chemical kinetics,rate of reaction,order of reaction,arrhenius,half life reaction",
 "rate of reaction,rate constant,order of reaction,molecularity,half life,first order,zero order,second order,pseudo first order,"
 "arrhenius,activation energy,collision theory,threshold energy,rate law,integrated rate,catalyst,temperature coefficient,"
 "rate determining step,elementary reaction,complex reaction,t1/2,t 1/2,concentration time,half-life,reaction mechanism,"
 "frequency factor,effective collision,ea,instantaneous rate,average rate,units of rate constant"),
("d-f-block", "The d- and f-Block Elements", "Chemistry",
 "d and f block elements,d block,f block,transition elements,lanthanoids,actinoids",
 "transition element,d block,f block,lanthanoid,actinoid,lanthanide,actinide,kmno4,k2cr2o7,potassium permanganate,"
 "potassium dichromate,chromate,dichromate,interstitial,alloy,magnetic moment,spin only,catalytic,coloured ions,"
 "variable oxidation,lanthanoid contraction,misch metal,ionisation enthalpy of transition,paramagnetic ion,"
 "mno4,cr2o7,inner transition,zn cd hg,colour of ions,disproportionation of mn,3d series,4d,5d,ln3+,aquated,aquated metal ions,unpaired electrons,qualitative analysis"),
("coordination-compounds", "Coordination Compounds", "Chemistry",
 "coordination compounds,complex compounds,werner,crystal field theory,ligand",
 "coordination,complex,ligand,werner,central metal,coordination number,chelate,edta,denticity,ambidentate,crystal field,"
 "cfse,octahedral complex,tetrahedral complex,square planar,high spin,low spin,spectrochemical,isomerism in complexes,"
 "linkage isomer,ionisation isomer,hydrate isomer,coordination isomer,effective atomic number,vbt,inner orbital,outer orbital,"
 "ferrocyanide,hexacyano,tetraammine,pentaammine,cisplatin,haemoglobin complex,chlorophyll complex,iupac name of complex,"
 "tetraammine,,carbonyl,octacarbonyl,triammine,amminechromium,chloridochromium"),
("haloalkanes-haloarenes", "Haloalkanes and Haloarenes", "Chemistry",
 "haloalkanes and haloarenes,alkyl halides,sn1,sn2,aryl halides",
 "haloalkane,haloarene,alkyl halide,aryl halide,sn1,sn2,nucleophilic substitution,elimination,walden,racemisation,"
 "retention,inversion,grignard,finkelstein,swarts,sandmeyer,gattermann,wurtz fittig,fittig,dehydrohalogenation,"
 "chloroform,iodoform,dichloromethane,ccl4,freons,ddt,carbylamine,chlorobenzene,bromoethane,optical rotation,"
 "halogen derivative,leaving group,saytzeff,polyhalogen,tetrachloromethane,hunsdiecker,bromide,butyl bromide,alkyl bromide,sodium methoxide,methyl ether"),
("alcohols-phenols-ethers", "Alcohols, Phenols and Ethers", "Chemistry",
 "alcohols phenols and ethers,alcohol,phenol,ether",
 "alcohol,phenol,ether,lucas,williamson,kolbe,reimer tiemann,esterification,dehydration,oxidation of alcohol,pcc,"
 "ethanol,methanol,glycerol,cresol,picric acid,salicylaldehyde,anisole,diethyl ether,acidity of phenol,hydroboration oxidation,"
 "cumene process,dow process,etherification,absolute alcohol,denatured,methoxy,ethoxy,ortho nitrophenol,azeotropic,"
 "primary alcohol,secondary alcohol,tertiary alcohol,victor meyer,zeisel,bakelite,aspirin"),
("aldehydes-ketones-acids", "Aldehydes, Ketones and Carboxylic Acids", "Chemistry",
 "aldehydes ketones and carboxylic acids,aldehydes,ketones,carboxylic acids,aldol",
 "aldehyde,ketone,carboxylic acid,aldol,cannizzaro,clemmensen,wolff kishner,tollens,fehling,benedict,rosenmund,stephen,"
 "etard,gattermann koch,friedel crafts acylation,hvz,hell volhard,acyl chloride,anhydride,ester,amide,decarboxylation,"
 "kolbe electrolysis,benzoic acid,formic acid,acetic acid,formaldehyde,acetaldehyde,acetone,benzaldehyde,acetophenone,"
 "nucleophilic addition,cyanohydrin,iodoform test,haloform,schiff,dnp,hydrazone,oxime,semicarbazone,carbonyl,"
 "acidity of carboxylic,esterification of acid,trans esterification,pinacol"),
("amines", "Amines", "Chemistry",
 "amines,aniline,diazonium,hoffmann,basicity of amines",
 "amine,aniline,diazonium,hoffmann,gabriel,carbylamine,hinsberg,sandmeyer,coupling,azo dye,basic strength of amine,"
 "primary amine,secondary amine,tertiary amine,quaternary,nitrobenzene,reduction of nitro,ammonolysis,acylation of aniline,"
 "bromination of aniline,diazotisation,nitrous acid,cyanide,isocyanide,methylamine,ethylamine,dimethylamine,trimethylamine,"
 "benzene diazonium,sulphanilic,amide to amine,hofmann bromamide,nitrile reduction,mendius"),
("p-block", "The p-Block Elements", "Chemistry",
 "p block elements,p block,group 15,group 16,group 17,group 18,nitrogen family,oxygen family,halogens,noble gases",
 "p block,nitrogen,ammonia,nitric acid,phosphorus,phosphine,oxoacid,oxygen,ozone,sulphur,sulphuric acid,so2,h2so4,"
 "halogen,chlorine,hydrogen chloride,interhalogen,noble gas,xenon,xef2,xef4,xef6,xeo3,argon,helium,boron,borax,"
 "diborane,aluminium,carbon,silicon,silicone,silicates,zeolite,boric acid,inert pair,allotrope,fullerene,graphite,diamond,"
 "bleaching powder,aqua regia,contact process,haber process,ostwald,oleum,pcl5,pcl3,ph3,h3po3,h3po4,hocl,hclo4,"
 "group 13,group 14,group 15,group 16,group 17,group 18,thallium,lead,tin,germanium,catenation,anomalous behaviour,"
 "magnetic nature of oxygen,sulphur dioxide,oxides of nitrogen,no2,n2o,nitrous,oxides,amphoteric,tl2o3,pbo,sno2"),
("s-block-hydrogen", "The s-Block Elements and Hydrogen", "Chemistry",
 "s block elements,hydrogen,alkali metals,alkaline earth metals",
 "s block,alkali metal,alkaline earth,sodium,potassium,lithium,calcium,magnesium,caesium,hydrogen peroxide,heavy water,"
 "deuterium,tritium,hydride,plaster of paris,gypsum,lime,quicklime,slaked lime,washing soda,baking soda,solvay,castner,"
 "flame test,hardness of water,temporary hardness,permanent hardness,calgon,hydrogen bonding in water,ionic hydride,"
 "covalent hydride,metallic hydride,electron deficient,syngas,water gas,dihydrogen,cement,portland,sodium carbonate,"),
("environmental-chem", "Environmental Chemistry", "Chemistry",
 "environmental chemistry,pollution chemistry,smog,acid rain",
 "environmental chemistry,pollutant,smog,acid rain,greenhouse,ozone depletion,cfcs,bod,cod,eutrophication,particulate,"
 "photochemical smog,pan,stratosphere,troposphere,green chemistry,dissolved oxygen,pesticide,"),
("polymers-everyday", "Polymers and Chemistry in Everyday Life", "Chemistry",
 "polymers,chemistry in everyday life,drugs medicine,soaps detergents",
 "polymer,monomer,polymerisation,addition polymer,condensation polymer,nylon,polyester,bakelite,teflon,pvc,polythene,"
 "neoprene,buna,natural rubber,vulcanisation,terylene,melamine,thermoplastic,thermosetting,biodegradable,pha,phbv,"
 "analgesic,antipyretic,antibiotic,antiseptic,disinfectant,antacid,antihistamine,tranquilliser,soap,detergent,"
 "sweetener,preservative,saponification,food additives,aspartame,saccharin,cationic detergent,anionic,non-ionic,"
 "chemotherapy,sulpha drug,broad spectrum,narrow spectrum,morphine,aspirin,paracetamol"),
("solid-state-surface", "Solid State and Surface Chemistry", "Chemistry",
 "solid state,surface chemistry,crystal lattice,adsorption,colloids",
 "unit cell,fcc,bcc,simple cubic,packing efficiency,coordination number in lattice,void,tetrahedral void,octahedral void,"
 "schottky,frenkel,f-centre,semiconductor doping,ferromagnetic,crystal lattice,close packing,hcp,ccp,density of unit cell,"
 "adsorption,absorption,physisorption,chemisorption,colloid,sol,emulsion,tyndall,brownian,coagulation,hardy schulze,"
 "micelle,cmc,catalysis,enzyme catalysis,freundlich,langmuir,electrophoresis,dialysis,peptisation,lyophilic,lyophobic"),
("metallurgy-general", "General Principles of Metallurgy", "Chemistry",
 "metallurgy,isolation of elements,extraction of metals,ores",
 "metallurgy,ore,concentration,roasting,calcination,smelting,flux,slag,froth floatation,leaching,electrolytic refining,"
 "zone refining,vapour phase refining,van arkel,mond process,ellingham,thermite,bessemer,blast furnace,cryolite,"
 "hall heroult,bauxite,haematite,malachite,zinc blende,galena,cinnabar,pig iron,cast iron,wrought iron,mineral,"),
]
