CREATE TABLE public.evals
(
    ods_type_activite text,
    categorie text,
    commune text,
    siret text,
    Nom text,
    numero_inspection text,
    geores text,
    filtre text,
    date_inspection text,
    code_postal text,
    evaluation text,
    adresse text,
    agrement text,
    lat text,
    lon text
);
\COPY evals FROM 'evals.csv' WITH (FORMAT CSV, HEADER);