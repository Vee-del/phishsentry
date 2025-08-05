--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS;
CREATE ROLE sentinel;
ALTER ROLE sentinel WITH NOSUPERUSER INHERIT NOCREATEROLE NOCREATEDB LOGIN NOREPLICATION NOBYPASSRLS PASSWORD 'SCRAM-SHA-256$4096:56mvHXrFyPGUKxHzCmXxDg==$GflLUDktKYCbCfehdp061S8T/mP184IzhlSPuUFOE8w=:jlklCQsPiPBGQC7O1Xla6GNz0oeeBwT0vWHM38kg1uo=';

--
-- User Configurations
--








--
-- Databases
--

--
-- Database "template1" dump
--

\connect template1

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3 (Debian 15.3-0+deb12u1)
-- Dumped by pg_dump version 15.3 (Debian 15.3-0+deb12u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- PostgreSQL database dump complete
--

--
-- Database "phishsentry" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3 (Debian 15.3-0+deb12u1)
-- Dumped by pg_dump version 15.3 (Debian 15.3-0+deb12u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: phishsentry; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE phishsentry WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';


ALTER DATABASE phishsentry OWNER TO postgres;

\connect phishsentry

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE phishsentry; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON DATABASE phishsentry TO sentinel;


--
-- PostgreSQL database dump complete
--

--
-- Database "phishsentry_db" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3 (Debian 15.3-0+deb12u1)
-- Dumped by pg_dump version 15.3 (Debian 15.3-0+deb12u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: phishsentry_db; Type: DATABASE; Schema: -; Owner: sentinel
--

CREATE DATABASE phishsentry_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';


ALTER DATABASE phishsentry_db OWNER TO sentinel;

\connect phishsentry_db

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: sentinel
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO sentinel;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: sentinel
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO sentinel;

--
-- Name: phishing_attempts; Type: TABLE; Schema: public; Owner: sentinel
--

CREATE TABLE public.phishing_attempts (
    id integer NOT NULL,
    sender character varying(100),
    subject character varying(200),
    received_at timestamp without time zone,
    body_preview character varying,
    verdict character varying
);


ALTER TABLE public.phishing_attempts OWNER TO sentinel;

--
-- Name: phishing_attempts_id_seq; Type: SEQUENCE; Schema: public; Owner: sentinel
--

CREATE SEQUENCE public.phishing_attempts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.phishing_attempts_id_seq OWNER TO sentinel;

--
-- Name: phishing_attempts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sentinel
--

ALTER SEQUENCE public.phishing_attempts_id_seq OWNED BY public.phishing_attempts.id;


--
-- Name: phishing_attempts id; Type: DEFAULT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.phishing_attempts ALTER COLUMN id SET DEFAULT nextval('public.phishing_attempts_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: sentinel
--

COPY public.alembic_version (version_num) FROM stdin;
04e5cdee36c1
\.


--
-- Data for Name: phishing_attempts; Type: TABLE DATA; Schema: public; Owner: sentinel
--

COPY public.phishing_attempts (id, sender, subject, received_at, body_preview, verdict) FROM stdin;
1	malicious@fakebank.com	Urgent: Account Suspended!	2025-06-24 20:00:40.469115	Click this link to verify your account...	\N
2	fakeme@gmail.com	You are seen!	2025-06-26 10:39:59.688443	We can see you everywhere!! Beware! 	\N
3	iamyou@we.com	sleep now	2025-06-26 11:00:02.984082	go to sleep	\N
4	google@org.com	“URGENT: Account Suspended”	2025-07-02 12:06:08.64073	“Please verify your account by clicking here”	\N
5	google@org.com	“URGENT: Account Suspended”	2025-07-02 12:09:44.293796	“Please verify your account by clicking here”	\N
6	googlemail.com	“URGENT: Account Suspended”	2025-07-02 12:20:44.040811	click here to confirm your account	\N
7	googlemail.com	“URGENT: Account Suspended”	2025-07-02 12:22:01.849252	click here to confirm your account	\N
8	googlemail.com	“URGENT: Account Suspended”	2025-07-02 13:13:25.634771	click here to confirm your account	\N
9	SAPcloud@gmail.urg	URGENT! Account Suspended	2025-07-02 13:14:57.466448	Click here to fix now	\N
\.


--
-- Name: phishing_attempts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sentinel
--

SELECT pg_catalog.setval('public.phishing_attempts_id_seq', 9, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: phishing_attempts phishing_attempts_pkey; Type: CONSTRAINT; Schema: public; Owner: sentinel
--

ALTER TABLE ONLY public.phishing_attempts
    ADD CONSTRAINT phishing_attempts_pkey PRIMARY KEY (id);


--
-- Name: ix_phishing_attempts_id; Type: INDEX; Schema: public; Owner: sentinel
--

CREATE INDEX ix_phishing_attempts_id ON public.phishing_attempts USING btree (id);


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON SEQUENCES  TO sentinel;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON TABLES  TO sentinel;


--
-- PostgreSQL database dump complete
--

--
-- Database "postgres" dump
--

\connect postgres

--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3 (Debian 15.3-0+deb12u1)
-- Dumped by pg_dump version 15.3 (Debian 15.3-0+deb12u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO sentinel;


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

