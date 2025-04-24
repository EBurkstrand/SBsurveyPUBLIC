CREATE TABLE SurveyResponses (
    id SERIAL NOT NULL,
    startTime timestamp default CURRENT_TIMESTAMP,
    responder text not null, 
    selection text not null,
    dropdown text not null,
    checkbox bool not null,
    sometimes text,
    primary key(id)
);