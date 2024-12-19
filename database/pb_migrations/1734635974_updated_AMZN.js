/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_2358460462")

  // update collection data
  unmarshal({
    "name": "AMZNRaw"
  }, collection)

  // remove field
  collection.fields.removeById("json3582863974")

  // remove field
  collection.fields.removeById("json578656804")

  // add field
  collection.fields.addAt(1, new Field({
    "hidden": false,
    "id": "json2918445923",
    "maxSize": 0,
    "name": "data",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "json"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_2358460462")

  // update collection data
  unmarshal({
    "name": "AMZN"
  }, collection)

  // add field
  collection.fields.addAt(1, new Field({
    "hidden": false,
    "id": "json3582863974",
    "maxSize": 0,
    "name": "ml",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "json"
  }))

  // add field
  collection.fields.addAt(2, new Field({
    "hidden": false,
    "id": "json578656804",
    "maxSize": 0,
    "name": "actual",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "json"
  }))

  // remove field
  collection.fields.removeById("json2918445923")

  return app.save(collection)
})
