CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "firstname" string,
  "lastname" string,
  "nickname" string,
  "email" string,
  "password" string,
  "image" string,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "follows" (
  "id" SERIAL PRIMARY KEY,
  "follower" int,
  "following" int,
  "created_at" timestamp
);

CREATE TABLE "locations" (
  "id" SERIAL PRIMARY KEY,
  "longitude" double,
  "latitude" double,
  "name" string,
  "description" text,
  "type" string,
  "size" int,
  "created_by" int,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "favorites" (
  "id" SERIAL PRIMARY KEY,
  "user_id" int,
  "location_id" int,
  "created_at" timestamp
);

CREATE TABLE "tags" (
  "id" SERIAL PRIMARY KEY,
  "location_id" int,
  "name" string,
  "created_at" timestamp
);

CREATE TABLE "reviews" (
  "id" SERIAL PRIMARY KEY,
  "user_id" int,
  "location_id" int,
  "grade" int,
  "comment" text,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "pets" (
  "id" SERIAL PRIMARY KEY,
  "owner" int,
  "name" string,
  "breed" string,
  "size" int,
  "energy" int,
  "image" string,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "pet_owners" (
  "id" SERIAL PRIMARY KEY,
  "owner_id" int,
  "pet_id" int
);

ALTER TABLE "follows" ADD FOREIGN KEY ("follower") REFERENCES "users" ("id");

ALTER TABLE "follows" ADD FOREIGN KEY ("following") REFERENCES "users" ("id");

ALTER TABLE "locations" ADD FOREIGN KEY ("created_by") REFERENCES "users" ("id");

ALTER TABLE "favorites" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "favorites" ADD FOREIGN KEY ("location_id") REFERENCES "locations" ("id");

ALTER TABLE "tags" ADD FOREIGN KEY ("location_id") REFERENCES "locations" ("id");

ALTER TABLE "reviews" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "reviews" ADD FOREIGN KEY ("location_id") REFERENCES "locations" ("id");

ALTER TABLE "pets" ADD FOREIGN KEY ("owner") REFERENCES "users" ("id");

ALTER TABLE "pet_owners" ADD FOREIGN KEY ("owner_id") REFERENCES "users" ("id");

ALTER TABLE "pet_owners" ADD FOREIGN KEY ("pet_id") REFERENCES "pets" ("id");
