CREATE TABLE IF NOT EXISTS `imdb` (
    `imdbID` TEXT NOT NULL PRIMARY KEY,
    `title` TEXT NOT NULL,
    `year` TEXT NOT NULL,
    `released` TEXT NOT NULL,
    `rated` TEXT NOT NULL,
    `genres` TEXT NOT NULL,
    `actors` TEXT NOT NULL,
    `directors` TEXT NOT NULL,
    `writers` TEXT NOT NULL,
    `plot` TEXT NOT NULL,
    `rating` REAL,
    `votes` INTEGER,
    `type` TEXT NOT NULL,
    `poster` TEXT NOT NULL,
    `time` INTEGER NOT NULL,
    `updated_at` DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `created_at` DATE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS types (
    type_id INTEGER NOT NULL PRIMARY KEY,
    type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS imdb_types (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    type_id INTEGER NOT NULL,
    imdbID TEXT NOT NULL,
    FOREIGN KEY(`type_id`) REFERENCES `types`(`type_id`),
    FOREIGN KEY(`imdbID`) REFERENCES `imdb`(`imdbID`)
);

CREATE TABLE IF NOT EXISTS genres (
    genre_id INTEGER NOT NULL PRIMARY KEY,
    genre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS imdb_genres (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    genre_id INTEGER NOT NULL,
    imdbID TEXT NOT NULL,
    FOREIGN KEY(`genre_id`) REFERENCES `genres`(`genre_id`),
    FOREIGN KEY(`imdbID`) REFERENCES `imdb`(`imdbID`)
);

CREATE TABLE IF NOT EXISTS actors (
    actor_id INTEGER NOT NULL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS `idx_imdb_imdbID` ON `imdb` (`imdbID`);
CREATE INDEX IF NOT EXISTS `idx_imdb_title` ON `imdb` (`title`);

CREATE INDEX IF NOT EXISTS `idx_imdb_imdbID` ON `imdb` (`imdbID`);
CREATE INDEX IF NOT EXISTS `idx_imdb_title` ON `imdb` (`title`);

CREATE TRIGGER UpdateLastTime AFTER UPDATE ON `imdb`
BEGIN
  UPDATE `imdb` SET `updated_at`=CURRENT_TIMESTAMP WHERE imdbID=id;
END;


-- `imdbID`, `title`, `year`, `released`, `rated`, `genres`, `actors`, `directors`, `writers`, `plot`, `rating`, `votes`, `type`, `poster`, `time`
