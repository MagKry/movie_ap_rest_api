# movie_app_rest_api
The development of cinema management app. To the existing endpoints:
    - /movies/ – GET i POST
    - movies/{id}/ – GET, PUT i DELETE.

The following endpoints have been added:
    - /cinemas:
        GET – returns the list of all cinemas,
        POST – creates a new cinema based on the posted data,
    - /cinemas/{id}:
        GET – displays info about the cinema of a given id,
        PUT – modifies info about the cinema of a given id,
        DELETE – deletes the cimena of a given id,
    - /screenings:
        GET – returns the list of all showings,
        POST – created a new showing based on the posted data,
    - /screenings/{id}:
        GET – displays info about the showing of a given id,
        PUT – modifies info about the showing of a given id,
        DELETE – deletes the showing of a given id.

The above was created with use of new models, views and serializes. The functionalties are covered with tests.
