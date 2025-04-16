--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.2

-- Started on 2025-04-16 21:54:22

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 217 (class 1259 OID 18846)
-- Name: достижение; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."достижение" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL,
    "описание" text
);


ALTER TABLE public."достижение" OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 18851)
-- Name: achievements_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.achievements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.achievements_id_seq OWNER TO postgres;

--
-- TOC entry 5463 (class 0 OID 0)
-- Dependencies: 218
-- Name: achievements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.achievements_id_seq OWNED BY public."достижение".id;


--
-- TOC entry 219 (class 1259 OID 18852)
-- Name: чат; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."чат" (
    id integer NOT NULL
);


ALTER TABLE public."чат" OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 18855)
-- Name: chat_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.chat_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.chat_id_seq OWNER TO postgres;

--
-- TOC entry 5464 (class 0 OID 0)
-- Dependencies: 220
-- Name: chat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.chat_id_seq OWNED BY public."чат".id;


--
-- TOC entry 221 (class 1259 OID 18856)
-- Name: клиент; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."клиент" (
    id integer NOT NULL,
    "уровень_подготовки_id" integer,
    "пользователь_id" integer NOT NULL
);


ALTER TABLE public."клиент" OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 18859)
-- Name: client_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.client_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.client_id_seq OWNER TO postgres;

--
-- TOC entry 5465 (class 0 OID 0)
-- Dependencies: 222
-- Name: client_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.client_id_seq OWNED BY public."клиент".id;


--
-- TOC entry 223 (class 1259 OID 18860)
-- Name: клиент_и_подписка; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."клиент_и_подписка" (
    "клиент_id" integer NOT NULL,
    id integer NOT NULL,
    "подписка_id" integer NOT NULL,
    "дата_начала" date NOT NULL,
    "дата_истечения" date NOT NULL,
    "статус_подписки_id" integer NOT NULL,
    "дата_паузы" date
);


ALTER TABLE public."клиент_и_подписка" OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 18863)
-- Name: client_subscription_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.client_subscription_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.client_subscription_id_seq OWNER TO postgres;

--
-- TOC entry 5466 (class 0 OID 0)
-- Dependencies: 224
-- Name: client_subscription_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.client_subscription_id_seq OWNED BY public."клиент_и_подписка".id;


--
-- TOC entry 225 (class 1259 OID 18864)
-- Name: тренер; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."тренер" (
    id integer NOT NULL,
    "пользователь_id" integer NOT NULL
);


ALTER TABLE public."тренер" OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 18867)
-- Name: coach_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.coach_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.coach_id_seq OWNER TO postgres;

--
-- TOC entry 5467 (class 0 OID 0)
-- Dependencies: 226
-- Name: coach_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.coach_id_seq OWNED BY public."тренер".id;


--
-- TOC entry 227 (class 1259 OID 18868)
-- Name: специальность_тренера; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."специальность_тренера" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL
);


ALTER TABLE public."специальность_тренера" OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 18871)
-- Name: coach_speciality_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.coach_speciality_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.coach_speciality_id_seq OWNER TO postgres;

--
-- TOC entry 5468 (class 0 OID 0)
-- Dependencies: 228
-- Name: coach_speciality_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.coach_speciality_id_seq OWNED BY public."специальность_тренера".id;


--
-- TOC entry 229 (class 1259 OID 18872)
-- Name: дневник; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."дневник" (
    id integer NOT NULL,
    "дата" date NOT NULL,
    "запись" text NOT NULL,
    "пользователь_id" integer NOT NULL,
    "файл_id" integer
);


ALTER TABLE public."дневник" OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 18877)
-- Name: diary_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.diary_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.diary_id_seq OWNER TO postgres;

--
-- TOC entry 5469 (class 0 OID 0)
-- Dependencies: 230
-- Name: diary_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.diary_id_seq OWNED BY public."дневник".id;


--
-- TOC entry 231 (class 1259 OID 18878)
-- Name: снаряжение; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."снаряжение" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL
);


ALTER TABLE public."снаряжение" OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 18881)
-- Name: equipment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.equipment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.equipment_id_seq OWNER TO postgres;

--
-- TOC entry 5470 (class 0 OID 0)
-- Dependencies: 232
-- Name: equipment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.equipment_id_seq OWNED BY public."снаряжение".id;


--
-- TOC entry 233 (class 1259 OID 18882)
-- Name: упражнение_и_мыщца; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."упражнение_и_мыщца" (
    "упражнение_id" integer NOT NULL,
    "мышца_id" integer NOT NULL,
    id integer NOT NULL,
    "приоритет_мышцы_id" integer NOT NULL
);


ALTER TABLE public."упражнение_и_мыщца" OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 18885)
-- Name: exercise_and_muscle_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.exercise_and_muscle_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.exercise_and_muscle_id_seq OWNER TO postgres;

--
-- TOC entry 5471 (class 0 OID 0)
-- Dependencies: 234
-- Name: exercise_and_muscle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.exercise_and_muscle_id_seq OWNED BY public."упражнение_и_мыщца".id;


--
-- TOC entry 235 (class 1259 OID 18886)
-- Name: сложность_упражнения; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."сложность_упражнения" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL
);


ALTER TABLE public."сложность_упражнения" OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 18889)
-- Name: exercise_difficulty_2_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.exercise_difficulty_2_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.exercise_difficulty_2_id_seq OWNER TO postgres;

--
-- TOC entry 5472 (class 0 OID 0)
-- Dependencies: 236
-- Name: exercise_difficulty_2_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.exercise_difficulty_2_id_seq OWNED BY public."сложность_упражнения".id;


--
-- TOC entry 237 (class 1259 OID 18890)
-- Name: упражнение; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."упражнение" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL,
    "описание" text,
    "тип_упражнения_id" integer NOT NULL,
    "сложность_упражнения_id" integer NOT NULL
);


ALTER TABLE public."упражнение" OWNER TO postgres;

--
-- TOC entry 238 (class 1259 OID 18895)
-- Name: exercise_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.exercise_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.exercise_id_seq OWNER TO postgres;

--
-- TOC entry 5473 (class 0 OID 0)
-- Dependencies: 238
-- Name: exercise_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.exercise_id_seq OWNED BY public."упражнение".id;


--
-- TOC entry 239 (class 1259 OID 18896)
-- Name: этап_упражнения; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."этап_упражнения" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL
);


ALTER TABLE public."этап_упражнения" OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 18899)
-- Name: exercise_stage_2_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.exercise_stage_2_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.exercise_stage_2_id_seq OWNER TO postgres;

--
-- TOC entry 5474 (class 0 OID 0)
-- Dependencies: 240
-- Name: exercise_stage_2_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.exercise_stage_2_id_seq OWNED BY public."этап_упражнения".id;


--
-- TOC entry 241 (class 1259 OID 18900)
-- Name: тип_упражнения; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."тип_упражнения" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL
);


ALTER TABLE public."тип_упражнения" OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 18903)
-- Name: exercise_type_2_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.exercise_type_2_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.exercise_type_2_id_seq OWNER TO postgres;

--
-- TOC entry 5475 (class 0 OID 0)
-- Dependencies: 242
-- Name: exercise_type_2_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.exercise_type_2_id_seq OWNED BY public."тип_упражнения".id;


--
-- TOC entry 243 (class 1259 OID 18904)
-- Name: чувство; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."чувство" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL
);


ALTER TABLE public."чувство" OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 18907)
-- Name: feeling_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.feeling_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.feeling_id_seq OWNER TO postgres;

--
-- TOC entry 5476 (class 0 OID 0)
-- Dependencies: 244
-- Name: feeling_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.feeling_id_seq OWNED BY public."чувство".id;


--
-- TOC entry 245 (class 1259 OID 18908)
-- Name: файл; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."файл" (
    id integer NOT NULL,
    "имя_файла" character varying(255)
);


ALTER TABLE public."файл" OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 18911)
-- Name: file_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.file_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.file_id_seq OWNER TO postgres;

--
-- TOC entry 5477 (class 0 OID 0)
-- Dependencies: 246
-- Name: file_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.file_id_seq OWNED BY public."файл".id;


--
-- TOC entry 247 (class 1259 OID 18912)
-- Name: тип_файла; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."тип_файла" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL
);


ALTER TABLE public."тип_файла" OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 18915)
-- Name: file_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.file_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.file_type_id_seq OWNER TO postgres;

--
-- TOC entry 5478 (class 0 OID 0)
-- Dependencies: 248
-- Name: file_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.file_type_id_seq OWNED BY public."тип_файла".id;


--
-- TOC entry 249 (class 1259 OID 18916)
-- Name: сообщение; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."сообщение" (
    id integer NOT NULL,
    "время_отправки" timestamp with time zone NOT NULL,
    "текст" text NOT NULL
);


ALTER TABLE public."сообщение" OWNER TO postgres;

--
-- TOC entry 250 (class 1259 OID 18921)
-- Name: message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.message_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.message_id_seq OWNER TO postgres;

--
-- TOC entry 5479 (class 0 OID 0)
-- Dependencies: 250
-- Name: message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.message_id_seq OWNED BY public."сообщение".id;


--
-- TOC entry 251 (class 1259 OID 18922)
-- Name: мышца; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."мышца" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL
);


ALTER TABLE public."мышца" OWNER TO postgres;

--
-- TOC entry 252 (class 1259 OID 18925)
-- Name: muscle_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.muscle_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.muscle_id_seq OWNER TO postgres;

--
-- TOC entry 5480 (class 0 OID 0)
-- Dependencies: 252
-- Name: muscle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.muscle_id_seq OWNED BY public."мышца".id;


--
-- TOC entry 253 (class 1259 OID 18926)
-- Name: приоритет_мышцы; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."приоритет_мышцы" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL
);


ALTER TABLE public."приоритет_мышцы" OWNER TO postgres;

--
-- TOC entry 254 (class 1259 OID 18929)
-- Name: muscle_priority_2_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.muscle_priority_2_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.muscle_priority_2_id_seq OWNER TO postgres;

--
-- TOC entry 5481 (class 0 OID 0)
-- Dependencies: 254
-- Name: muscle_priority_2_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.muscle_priority_2_id_seq OWNED BY public."приоритет_мышцы".id;


--
-- TOC entry 255 (class 1259 OID 18930)
-- Name: питание; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."питание" (
    id integer NOT NULL,
    "калории" integer NOT NULL,
    "белки" integer,
    "жиры" integer,
    "углеводы" integer,
    "пользователь_id" integer NOT NULL
);


ALTER TABLE public."питание" OWNER TO postgres;

--
-- TOC entry 256 (class 1259 OID 18933)
-- Name: nutrition_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.nutrition_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.nutrition_id_seq OWNER TO postgres;

--
-- TOC entry 5482 (class 0 OID 0)
-- Dependencies: 256
-- Name: nutrition_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.nutrition_id_seq OWNED BY public."питание".id;


--
-- TOC entry 257 (class 1259 OID 18934)
-- Name: цель_тренировок; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."цель_тренировок" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL
);


ALTER TABLE public."цель_тренировок" OWNER TO postgres;

--
-- TOC entry 258 (class 1259 OID 18937)
-- Name: purpose_of_workouts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.purpose_of_workouts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.purpose_of_workouts_id_seq OWNER TO postgres;

--
-- TOC entry 5483 (class 0 OID 0)
-- Dependencies: 258
-- Name: purpose_of_workouts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.purpose_of_workouts_id_seq OWNED BY public."цель_тренировок".id;


--
-- TOC entry 259 (class 1259 OID 18938)
-- Name: причина_чувства; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."причина_чувства" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL
);


ALTER TABLE public."причина_чувства" OWNER TO postgres;

--
-- TOC entry 260 (class 1259 OID 18941)
-- Name: reason_of_feeling_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reason_of_feeling_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reason_of_feeling_id_seq OWNER TO postgres;

--
-- TOC entry 5484 (class 0 OID 0)
-- Dependencies: 260
-- Name: reason_of_feeling_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reason_of_feeling_id_seq OWNED BY public."причина_чувства".id;


--
-- TOC entry 261 (class 1259 OID 18942)
-- Name: шаги; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."шаги" (
    id integer NOT NULL,
    "колво" integer NOT NULL,
    "целевое_колво" integer,
    "дата" date NOT NULL,
    "пользователь_id" integer NOT NULL
);


ALTER TABLE public."шаги" OWNER TO postgres;

--
-- TOC entry 262 (class 1259 OID 18945)
-- Name: steps_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.steps_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.steps_id_seq OWNER TO postgres;

--
-- TOC entry 5485 (class 0 OID 0)
-- Dependencies: 262
-- Name: steps_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.steps_id_seq OWNED BY public."шаги".id;


--
-- TOC entry 263 (class 1259 OID 18946)
-- Name: подписка; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."подписка" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL,
    "цена" integer NOT NULL,
    "срок_действия" integer NOT NULL
);


ALTER TABLE public."подписка" OWNER TO postgres;

--
-- TOC entry 264 (class 1259 OID 18949)
-- Name: subscription_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subscription_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subscription_id_seq OWNER TO postgres;

--
-- TOC entry 5486 (class 0 OID 0)
-- Dependencies: 264
-- Name: subscription_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subscription_id_seq OWNED BY public."подписка".id;


--
-- TOC entry 265 (class 1259 OID 18950)
-- Name: статус_подписки; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."статус_подписки" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL
);


ALTER TABLE public."статус_подписки" OWNER TO postgres;

--
-- TOC entry 266 (class 1259 OID 18953)
-- Name: subscription_status_2_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subscription_status_2_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subscription_status_2_id_seq OWNER TO postgres;

--
-- TOC entry 5487 (class 0 OID 0)
-- Dependencies: 266
-- Name: subscription_status_2_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subscription_status_2_id_seq OWNED BY public."статус_подписки".id;


--
-- TOC entry 267 (class 1259 OID 18954)
-- Name: уровень_тренировки; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."уровень_тренировки" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL
);


ALTER TABLE public."уровень_тренировки" OWNER TO postgres;

--
-- TOC entry 268 (class 1259 OID 18957)
-- Name: training_level_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.training_level_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.training_level_id_seq OWNER TO postgres;

--
-- TOC entry 5488 (class 0 OID 0)
-- Dependencies: 268
-- Name: training_level_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.training_level_id_seq OWNED BY public."уровень_тренировки".id;


--
-- TOC entry 269 (class 1259 OID 18958)
-- Name: пользователь; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."пользователь" (
    id integer NOT NULL,
    "дата_рождения" date,
    "хэш_пароля" character varying(255) NOT NULL,
    "почта" character varying(255) NOT NULL,
    "отчество" character varying(255),
    "фамилия" character varying(255),
    "имя" character varying(255),
    "пол_id" integer
);


ALTER TABLE public."пользователь" OWNER TO postgres;

--
-- TOC entry 270 (class 1259 OID 18963)
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO postgres;

--
-- TOC entry 5489 (class 0 OID 0)
-- Dependencies: 270
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."пользователь".id;


--
-- TOC entry 271 (class 1259 OID 18964)
-- Name: вода; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."вода" (
    id integer NOT NULL,
    "объем" integer NOT NULL,
    "целевой_объем" integer,
    "дата" date NOT NULL,
    "пользователь_id" integer NOT NULL
);


ALTER TABLE public."вода" OWNER TO postgres;

--
-- TOC entry 272 (class 1259 OID 18967)
-- Name: water_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.water_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.water_id_seq OWNER TO postgres;

--
-- TOC entry 5490 (class 0 OID 0)
-- Dependencies: 272
-- Name: water_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.water_id_seq OWNED BY public."вода".id;


--
-- TOC entry 273 (class 1259 OID 18968)
-- Name: вес; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."вес" (
    "вес" integer NOT NULL,
    id integer NOT NULL,
    "дата" date NOT NULL,
    "пользователь_id" integer NOT NULL
);


ALTER TABLE public."вес" OWNER TO postgres;

--
-- TOC entry 274 (class 1259 OID 18971)
-- Name: weight_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.weight_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.weight_id_seq OWNER TO postgres;

--
-- TOC entry 5491 (class 0 OID 0)
-- Dependencies: 274
-- Name: weight_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.weight_id_seq OWNED BY public."вес".id;


--
-- TOC entry 275 (class 1259 OID 18972)
-- Name: тренировка_и_упражнение; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."тренировка_и_упражнение" (
    id integer NOT NULL,
    "тренировка_id" integer NOT NULL,
    "упражнение_id" integer NOT NULL,
    "номер_в_очереди" integer NOT NULL,
    "колво_подходов" integer NOT NULL,
    "колво_подходов_выполнено" integer NOT NULL,
    "колво_повторений" integer NOT NULL,
    "колво_повторений_выполнено" integer NOT NULL,
    "этап_упражнения_id" integer NOT NULL
);


ALTER TABLE public."тренировка_и_упражнение" OWNER TO postgres;

--
-- TOC entry 276 (class 1259 OID 18975)
-- Name: workout_and_exercise_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.workout_and_exercise_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.workout_and_exercise_id_seq OWNER TO postgres;

--
-- TOC entry 5492 (class 0 OID 0)
-- Dependencies: 276
-- Name: workout_and_exercise_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.workout_and_exercise_id_seq OWNED BY public."тренировка_и_упражнение".id;


--
-- TOC entry 277 (class 1259 OID 18976)
-- Name: тренировка; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."тренировка" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL,
    "является_онлайн" boolean,
    "время_начала" timestamp with time zone,
    "чат_id" integer NOT NULL
);


ALTER TABLE public."тренировка" OWNER TO postgres;

--
-- TOC entry 278 (class 1259 OID 18979)
-- Name: workout_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.workout_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.workout_id_seq OWNER TO postgres;

--
-- TOC entry 5493 (class 0 OID 0)
-- Dependencies: 278
-- Name: workout_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.workout_id_seq OWNED BY public."тренировка".id;


--
-- TOC entry 279 (class 1259 OID 18980)
-- Name: план_тренировки; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."план_тренировки" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL,
    "описание" text
);


ALTER TABLE public."план_тренировки" OWNER TO postgres;

--
-- TOC entry 280 (class 1259 OID 18985)
-- Name: workout_plan_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.workout_plan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.workout_plan_id_seq OWNER TO postgres;

--
-- TOC entry 5494 (class 0 OID 0)
-- Dependencies: 280
-- Name: workout_plan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.workout_plan_id_seq OWNED BY public."план_тренировки".id;


--
-- TOC entry 281 (class 1259 OID 18986)
-- Name: тип_тренировки; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."тип_тренировки" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL
);


ALTER TABLE public."тип_тренировки" OWNER TO postgres;

--
-- TOC entry 282 (class 1259 OID 18989)
-- Name: workout_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.workout_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.workout_type_id_seq OWNER TO postgres;

--
-- TOC entry 5495 (class 0 OID 0)
-- Dependencies: 282
-- Name: workout_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.workout_type_id_seq OWNED BY public."тип_тренировки".id;


--
-- TOC entry 283 (class 1259 OID 18990)
-- Name: дневник_и_причина_чувства; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."дневник_и_причина_чувства" (
    "дневник_id" integer NOT NULL,
    "причина_чувства_id" integer NOT NULL
);


ALTER TABLE public."дневник_и_причина_чувства" OWNER TO postgres;

--
-- TOC entry 284 (class 1259 OID 18993)
-- Name: дневник_и_чувство; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."дневник_и_чувство" (
    "дневник_id" integer NOT NULL,
    "чувство_id" integer NOT NULL
);


ALTER TABLE public."дневник_и_чувство" OWNER TO postgres;

--
-- TOC entry 285 (class 1259 OID 18996)
-- Name: пол; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."пол" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL
);


ALTER TABLE public."пол" OWNER TO postgres;

--
-- TOC entry 286 (class 1259 OID 18999)
-- Name: имя_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."имя_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."имя_id_seq" OWNER TO postgres;

--
-- TOC entry 5496 (class 0 OID 0)
-- Dependencies: 286
-- Name: имя_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."имя_id_seq" OWNED BY public."пол".id;


--
-- TOC entry 287 (class 1259 OID 19000)
-- Name: клиент_и_тип_тренировки; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."клиент_и_тип_тренировки" (
    "клиент_id" integer NOT NULL,
    "тип_тренировки_id" integer NOT NULL
);


ALTER TABLE public."клиент_и_тип_тренировки" OWNER TO postgres;

--
-- TOC entry 288 (class 1259 OID 19003)
-- Name: клиент_и_цель_тренировок; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."клиент_и_цель_тренировок" (
    "клиент_id" integer NOT NULL,
    "цель_тренировок_id" integer NOT NULL
);


ALTER TABLE public."клиент_и_цель_тренировок" OWNER TO postgres;

--
-- TOC entry 289 (class 1259 OID 19006)
-- Name: отзыв; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."отзыв" (
    "клиент_id" integer NOT NULL,
    "тренер_id" integer NOT NULL,
    "рейтинг" numeric NOT NULL,
    CONSTRAINT feedback_rating_chk CHECK ((("рейтинг" >= 0.0) AND ("рейтинг" <= 5.0)))
);


ALTER TABLE public."отзыв" OWNER TO postgres;

--
-- TOC entry 290 (class 1259 OID 19012)
-- Name: план_тренировки_и_пользователь; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."план_тренировки_и_пользователь" (
    "пользователь_id" integer NOT NULL,
    "план_тренировки_id" integer NOT NULL
);


ALTER TABLE public."план_тренировки_и_пользователь" OWNER TO postgres;

--
-- TOC entry 291 (class 1259 OID 19015)
-- Name: пользователь_и_достижение; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."пользователь_и_достижение" (
    "пользователь_id" integer NOT NULL,
    "достижение_id" integer NOT NULL
);


ALTER TABLE public."пользователь_и_достижение" OWNER TO postgres;

--
-- TOC entry 292 (class 1259 OID 19018)
-- Name: сообщение_и_файл; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."сообщение_и_файл" (
    "сообщение_id" integer NOT NULL,
    "файл_id" integer NOT NULL
);


ALTER TABLE public."сообщение_и_файл" OWNER TO postgres;

--
-- TOC entry 293 (class 1259 OID 19021)
-- Name: тренер_и_клиент; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."тренер_и_клиент" (
    "тренер_id" integer NOT NULL,
    "клиент_id" integer NOT NULL
);


ALTER TABLE public."тренер_и_клиент" OWNER TO postgres;

--
-- TOC entry 294 (class 1259 OID 19024)
-- Name: тренер_и_специальность; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."тренер_и_специальность" (
    "тренер_id" integer NOT NULL,
    "специальность_тренера_id" integer NOT NULL
);


ALTER TABLE public."тренер_и_специальность" OWNER TO postgres;

--
-- TOC entry 295 (class 1259 OID 19027)
-- Name: тренировка_и_план_тренировки; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."тренировка_и_план_тренировки" (
    "тренировка_id" integer NOT NULL,
    "план_тренировки_id" integer NOT NULL
);


ALTER TABLE public."тренировка_и_план_тренировки" OWNER TO postgres;

--
-- TOC entry 296 (class 1259 OID 19030)
-- Name: тренировка_и_пользователь; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."тренировка_и_пользователь" (
    "пользователь_id" integer NOT NULL,
    "тренировка_id" integer NOT NULL
);


ALTER TABLE public."тренировка_и_пользователь" OWNER TO postgres;

--
-- TOC entry 297 (class 1259 OID 19033)
-- Name: упражнение_и_пользователь; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."упражнение_и_пользователь" (
    "упражнение_id" integer NOT NULL,
    "пользователь_id" integer NOT NULL
);


ALTER TABLE public."упражнение_и_пользователь" OWNER TO postgres;

--
-- TOC entry 298 (class 1259 OID 19036)
-- Name: упражнение_и_снаряжение; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."упражнение_и_снаряжение" (
    "упражнение_id" integer NOT NULL,
    "снаряжение_id" integer NOT NULL
);


ALTER TABLE public."упражнение_и_снаряжение" OWNER TO postgres;

--
-- TOC entry 299 (class 1259 OID 19039)
-- Name: упражнение_и_файл; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."упражнение_и_файл" (
    "упражнение_id" integer NOT NULL,
    "файл_id" integer NOT NULL
);


ALTER TABLE public."упражнение_и_файл" OWNER TO postgres;

--
-- TOC entry 300 (class 1259 OID 19042)
-- Name: уровень_подготовки; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."уровень_подготовки" (
    id integer NOT NULL,
    "название" character varying(255) NOT NULL,
    CONSTRAINT chk_name CHECK ((("название")::text ~ '^[А-Яа-яёЁ]+$'::text))
);


ALTER TABLE public."уровень_подготовки" OWNER TO postgres;

--
-- TOC entry 301 (class 1259 OID 19046)
-- Name: уровень_подготовки_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."уровень_подготовки_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."уровень_подготовки_id_seq" OWNER TO postgres;

--
-- TOC entry 5497 (class 0 OID 0)
-- Dependencies: 301
-- Name: уровень_подготовки_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."уровень_подготовки_id_seq" OWNED BY public."уровень_подготовки".id;


--
-- TOC entry 302 (class 1259 OID 19047)
-- Name: файл_и_тип_файла; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."файл_и_тип_файла" (
    "файл_id" integer NOT NULL,
    "тип_файла_id" integer NOT NULL
);


ALTER TABLE public."файл_и_тип_файла" OWNER TO postgres;

--
-- TOC entry 303 (class 1259 OID 19050)
-- Name: чат_и_пользователь; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."чат_и_пользователь" (
    "пользователь_id" integer NOT NULL,
    "чат_id" integer NOT NULL
);


ALTER TABLE public."чат_и_пользователь" OWNER TO postgres;

--
-- TOC entry 4961 (class 2604 OID 19053)
-- Name: вес id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."вес" ALTER COLUMN id SET DEFAULT nextval('public.weight_id_seq'::regclass);


--
-- TOC entry 4960 (class 2604 OID 19054)
-- Name: вода id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."вода" ALTER COLUMN id SET DEFAULT nextval('public.water_id_seq'::regclass);


--
-- TOC entry 4939 (class 2604 OID 19055)
-- Name: дневник id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."дневник" ALTER COLUMN id SET DEFAULT nextval('public.diary_id_seq'::regclass);


--
-- TOC entry 4933 (class 2604 OID 19056)
-- Name: достижение id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."достижение" ALTER COLUMN id SET DEFAULT nextval('public.achievements_id_seq'::regclass);


--
-- TOC entry 4935 (class 2604 OID 19057)
-- Name: клиент id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."клиент" ALTER COLUMN id SET DEFAULT nextval('public.client_id_seq'::regclass);


--
-- TOC entry 4936 (class 2604 OID 19058)
-- Name: клиент_и_подписка id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."клиент_и_подписка" ALTER COLUMN id SET DEFAULT nextval('public.client_subscription_id_seq'::regclass);


--
-- TOC entry 4950 (class 2604 OID 19059)
-- Name: мышца id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."мышца" ALTER COLUMN id SET DEFAULT nextval('public.muscle_id_seq'::regclass);


--
-- TOC entry 4952 (class 2604 OID 19060)
-- Name: питание id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."питание" ALTER COLUMN id SET DEFAULT nextval('public.nutrition_id_seq'::regclass);


--
-- TOC entry 4964 (class 2604 OID 19061)
-- Name: план_тренировки id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."план_тренировки" ALTER COLUMN id SET DEFAULT nextval('public.workout_plan_id_seq'::regclass);


--
-- TOC entry 4956 (class 2604 OID 19062)
-- Name: подписка id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."подписка" ALTER COLUMN id SET DEFAULT nextval('public.subscription_id_seq'::regclass);


--
-- TOC entry 4966 (class 2604 OID 19063)
-- Name: пол id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."пол" ALTER COLUMN id SET DEFAULT nextval('public."имя_id_seq"'::regclass);


--
-- TOC entry 4959 (class 2604 OID 19064)
-- Name: пользователь id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."пользователь" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- TOC entry 4951 (class 2604 OID 19065)
-- Name: приоритет_мышцы id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."приоритет_мышцы" ALTER COLUMN id SET DEFAULT nextval('public.muscle_priority_2_id_seq'::regclass);


--
-- TOC entry 4954 (class 2604 OID 19066)
-- Name: причина_чувства id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."причина_чувства" ALTER COLUMN id SET DEFAULT nextval('public.reason_of_feeling_id_seq'::regclass);


--
-- TOC entry 4942 (class 2604 OID 19067)
-- Name: сложность_упражнения id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."сложность_упражнения" ALTER COLUMN id SET DEFAULT nextval('public.exercise_difficulty_2_id_seq'::regclass);


--
-- TOC entry 4940 (class 2604 OID 19068)
-- Name: снаряжение id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."снаряжение" ALTER COLUMN id SET DEFAULT nextval('public.equipment_id_seq'::regclass);


--
-- TOC entry 4949 (class 2604 OID 19069)
-- Name: сообщение id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."сообщение" ALTER COLUMN id SET DEFAULT nextval('public.message_id_seq'::regclass);


--
-- TOC entry 4938 (class 2604 OID 19070)
-- Name: специальность_тренера id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."специальность_тренера" ALTER COLUMN id SET DEFAULT nextval('public.coach_speciality_id_seq'::regclass);


--
-- TOC entry 4957 (class 2604 OID 19071)
-- Name: статус_подписки id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."статус_подписки" ALTER COLUMN id SET DEFAULT nextval('public.subscription_status_2_id_seq'::regclass);


--
-- TOC entry 4965 (class 2604 OID 19072)
-- Name: тип_тренировки id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тип_тренировки" ALTER COLUMN id SET DEFAULT nextval('public.workout_type_id_seq'::regclass);


--
-- TOC entry 4945 (class 2604 OID 19073)
-- Name: тип_упражнения id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тип_упражнения" ALTER COLUMN id SET DEFAULT nextval('public.exercise_type_2_id_seq'::regclass);


--
-- TOC entry 4948 (class 2604 OID 19074)
-- Name: тип_файла id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тип_файла" ALTER COLUMN id SET DEFAULT nextval('public.file_type_id_seq'::regclass);


--
-- TOC entry 4937 (class 2604 OID 19075)
-- Name: тренер id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренер" ALTER COLUMN id SET DEFAULT nextval('public.coach_id_seq'::regclass);


--
-- TOC entry 4963 (class 2604 OID 19076)
-- Name: тренировка id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренировка" ALTER COLUMN id SET DEFAULT nextval('public.workout_id_seq'::regclass);


--
-- TOC entry 4962 (class 2604 OID 19077)
-- Name: тренировка_и_упражнение id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренировка_и_упражнение" ALTER COLUMN id SET DEFAULT nextval('public.workout_and_exercise_id_seq'::regclass);


--
-- TOC entry 4943 (class 2604 OID 19078)
-- Name: упражнение id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."упражнение" ALTER COLUMN id SET DEFAULT nextval('public.exercise_id_seq'::regclass);


--
-- TOC entry 4941 (class 2604 OID 19079)
-- Name: упражнение_и_мыщца id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."упражнение_и_мыщца" ALTER COLUMN id SET DEFAULT nextval('public.exercise_and_muscle_id_seq'::regclass);


--
-- TOC entry 4967 (class 2604 OID 19080)
-- Name: уровень_подготовки id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."уровень_подготовки" ALTER COLUMN id SET DEFAULT nextval('public."уровень_подготовки_id_seq"'::regclass);


--
-- TOC entry 4958 (class 2604 OID 19081)
-- Name: уровень_тренировки id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."уровень_тренировки" ALTER COLUMN id SET DEFAULT nextval('public.training_level_id_seq'::regclass);


--
-- TOC entry 4947 (class 2604 OID 19082)
-- Name: файл id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."файл" ALTER COLUMN id SET DEFAULT nextval('public.file_id_seq'::regclass);


--
-- TOC entry 4953 (class 2604 OID 19083)
-- Name: цель_тренировок id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."цель_тренировок" ALTER COLUMN id SET DEFAULT nextval('public.purpose_of_workouts_id_seq'::regclass);


--
-- TOC entry 4934 (class 2604 OID 19084)
-- Name: чат id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."чат" ALTER COLUMN id SET DEFAULT nextval('public.chat_id_seq'::regclass);


--
-- TOC entry 4946 (class 2604 OID 19085)
-- Name: чувство id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."чувство" ALTER COLUMN id SET DEFAULT nextval('public.feeling_id_seq'::regclass);


--
-- TOC entry 4955 (class 2604 OID 19086)
-- Name: шаги id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."шаги" ALTER COLUMN id SET DEFAULT nextval('public.steps_id_seq'::regclass);


--
-- TOC entry 4944 (class 2604 OID 19087)
-- Name: этап_упражнения id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."этап_упражнения" ALTER COLUMN id SET DEFAULT nextval('public.exercise_stage_2_id_seq'::regclass);


--
-- TOC entry 5427 (class 0 OID 18968)
-- Dependencies: 273
-- Data for Name: вес; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."вес" ("вес", id, "дата", "пользователь_id") FROM stdin;
70	1	2023-01-01	1
75	2	2023-01-02	2
80	3	2023-01-03	3
65	4	2023-01-04	4
90	5	2023-01-05	5
85	6	2023-01-06	6
78	7	2023-01-07	7
82	8	2023-01-08	8
68	9	2023-01-09	9
72	10	2023-01-10	10
\.


--
-- TOC entry 5425 (class 0 OID 18964)
-- Dependencies: 271
-- Data for Name: вода; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."вода" (id, "объем", "целевой_объем", "дата", "пользователь_id") FROM stdin;
1	500	1000	2023-01-01	1
2	600	1000	2023-01-02	2
3	700	1200	2023-01-03	3
4	800	1200	2023-01-04	4
5	900	1500	2023-01-05	5
6	1000	1500	2023-01-06	6
7	1100	1600	2023-01-07	7
8	1200	1600	2023-01-08	8
10	1400	1700	2023-01-10	10
9	1300	1700	2023-01-09	1
\.


--
-- TOC entry 5383 (class 0 OID 18872)
-- Dependencies: 229
-- Data for Name: дневник; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."дневник" (id, "дата", "запись", "пользователь_id", "файл_id") FROM stdin;
1	2023-02-01	Запись 1	1	1
2	2023-02-02	Запись 2	2	2
3	2023-02-03	Запись 3	3	3
4	2023-02-04	Запись 4	4	4
5	2023-02-05	Запись 5	5	5
6	2023-02-06	Запись 6	6	6
7	2023-02-07	Запись 7	7	7
8	2023-02-08	Запись 8	8	8
10	2023-02-10	Запись 10	10	10
11	2025-04-16	string	1	1
12	2025-04-16	string	1	1
13	2025-04-16	string	1	1
14	2025-04-16	string	1	1
17	2025-04-16	string	1	1
18	2025-04-16	string	1	1
16	2025-04-10	ng	2	2
19	2025-04-16	ывап	1	\N
20	2025-04-16	аааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааааа	1	\N
21	2025-04-16	ббббббббббббаааааааааааааааааааааааааа	1	\N
\.


--
-- TOC entry 5437 (class 0 OID 18990)
-- Dependencies: 283
-- Data for Name: дневник_и_причина_чувства; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."дневник_и_причина_чувства" ("дневник_id", "причина_чувства_id") FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
10	10
11	1
12	1
13	1
14	1
17	1
18	1
16	2
19	1
19	2
19	3
20	3
21	10
21	7
\.


--
-- TOC entry 5438 (class 0 OID 18993)
-- Dependencies: 284
-- Data for Name: дневник_и_чувство; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."дневник_и_чувство" ("дневник_id", "чувство_id") FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
10	10
11	1
12	1
13	1
14	1
17	1
18	1
16	2
19	1
19	2
19	3
20	3
21	10
21	4
\.


--
-- TOC entry 5371 (class 0 OID 18846)
-- Dependencies: 217
-- Data for Name: достижение; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."достижение" (id, "название", "описание") FROM stdin;
1	Достижение 1	Описание 1
2	Достижение 2	Описание 2
3	Достижение 3	Описание 3
4	Достижение 4	Описание 4
5	Достижение 5	Описание 5
6	Достижение 6	Описание 6
7	Достижение 7	Описание 7
8	Достижение 8	Описание 8
9	Достижение 9	Описание 9
10	Достижение 10	Описание 10
\.


--
-- TOC entry 5375 (class 0 OID 18856)
-- Dependencies: 221
-- Data for Name: клиент; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."клиент" (id, "уровень_подготовки_id", "пользователь_id") FROM stdin;
1	1	1
2	2	2
3	3	3
4	1	4
5	2	5
6	3	6
7	1	7
8	2	8
9	3	9
10	1	10
\.


--
-- TOC entry 5377 (class 0 OID 18860)
-- Dependencies: 223
-- Data for Name: клиент_и_подписка; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."клиент_и_подписка" ("клиент_id", id, "подписка_id", "дата_начала", "дата_истечения", "статус_подписки_id", "дата_паузы") FROM stdin;
1	1	1	2023-03-01	2023-04-01	1	2023-03-15
2	2	2	2023-03-02	2023-04-02	2	2023-03-16
3	3	3	2023-03-03	2023-04-03	3	2023-03-17
4	4	1	2023-03-04	2023-04-04	1	2023-03-18
5	5	2	2023-03-05	2023-04-05	3	2023-03-19
6	6	3	2023-03-06	2023-04-06	2	2023-03-20
7	7	1	2023-03-07	2023-04-07	3	2023-03-21
8	8	2	2023-03-08	2023-04-08	1	2023-03-22
9	9	3	2023-03-09	2023-04-09	2	2023-03-23
10	10	1	2023-03-10	2023-04-10	1	2023-03-24
\.


--
-- TOC entry 5441 (class 0 OID 19000)
-- Dependencies: 287
-- Data for Name: клиент_и_тип_тренировки; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."клиент_и_тип_тренировки" ("клиент_id", "тип_тренировки_id") FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
\.


--
-- TOC entry 5442 (class 0 OID 19003)
-- Dependencies: 288
-- Data for Name: клиент_и_цель_тренировок; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."клиент_и_цель_тренировок" ("клиент_id", "цель_тренировок_id") FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
\.


--
-- TOC entry 5405 (class 0 OID 18922)
-- Dependencies: 251
-- Data for Name: мышца; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."мышца" (id, "название") FROM stdin;
1	Бицепс
2	Трицепс
3	Квадрицепс
4	Задняя
5	Грудь
6	Плечи
7	Спина
8	Пресс
9	Икры
10	Бедра
\.


--
-- TOC entry 5443 (class 0 OID 19006)
-- Dependencies: 289
-- Data for Name: отзыв; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."отзыв" ("клиент_id", "тренер_id", "рейтинг") FROM stdin;
1	1	4.5
2	2	3.8
3	3	5.0
4	4	4.0
5	5	3.5
6	6	4.2
7	7	4.7
8	8	3.9
9	9	4.8
10	10	4.1
\.


--
-- TOC entry 5409 (class 0 OID 18930)
-- Dependencies: 255
-- Data for Name: питание; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."питание" (id, "калории", "белки", "жиры", "углеводы", "пользователь_id") FROM stdin;
1	2000	100	50	300	1
2	2100	110	55	310	2
3	2200	120	60	320	3
4	2300	130	65	330	4
5	2400	140	70	340	5
6	2500	150	75	350	6
7	2600	160	80	360	7
8	2700	170	85	370	8
9	2800	180	90	380	9
10	2900	190	95	390	10
\.


--
-- TOC entry 5433 (class 0 OID 18980)
-- Dependencies: 279
-- Data for Name: план_тренировки; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."план_тренировки" (id, "название", "описание") FROM stdin;
1	План 1	Описание плана 1
2	План 2	Описание плана 2
3	План 3	Описание плана 3
4	План 4	Описание плана 4
5	План 5	Описание плана 5
6	План 6	Описание плана 6
7	План 7	Описание плана 7
8	План 8	Описание плана 8
9	План 9	Описание плана 9
10	План 10	Описание плана 10
\.


--
-- TOC entry 5444 (class 0 OID 19012)
-- Dependencies: 290
-- Data for Name: план_тренировки_и_пользователь; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."план_тренировки_и_пользователь" ("пользователь_id", "план_тренировки_id") FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
1	2
\.


--
-- TOC entry 5417 (class 0 OID 18946)
-- Dependencies: 263
-- Data for Name: подписка; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."подписка" (id, "название", "цена", "срок_действия") FROM stdin;
1	Базовая	100	30
2	Стандарт	200	60
3	Премиум	300	90
4	Эконом	80	20
5	Оптимум	150	45
6	Профи	250	75
7	Макси	350	90
8	Ультра	450	100
9	VIP	550	120
10	Эксклюзив	650	150
\.


--
-- TOC entry 5439 (class 0 OID 18996)
-- Dependencies: 285
-- Data for Name: пол; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."пол" (id, "название") FROM stdin;
1	Мужской
2	Женский
\.


--
-- TOC entry 5423 (class 0 OID 18958)
-- Dependencies: 269
-- Data for Name: пользователь; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."пользователь" (id, "дата_рождения", "хэш_пароля", "почта", "отчество", "фамилия", "имя", "пол_id") FROM stdin;
1	1990-01-01	hash1	user1@example.com	Отчество	Иванов	Иван	1
2	1991-02-02	hash2	user2@example.com	Отчество	Петров	Петр	2
3	1992-03-03	hash3	user3@example.com	Отчество	Сидоров	Сидор	1
4	1993-04-04	hash4	user4@example.com	Отчество	Козлов	Алексей	2
5	1994-05-05	hash5	user5@example.com	Отчество	Морозов	Дмитрий	1
6	1995-06-06	hash6	user6@example.com	Отчество	Смирнов	Сергей	2
7	1996-07-07	hash7	user7@example.com	Отчество	Попов	Николай	1
8	1997-08-08	hash8	user8@example.com	Отчество	Васильев	Василий	2
9	1998-09-09	hash9	user9@example.com	Отчество	Соколов	Андрей	1
10	1999-10-10	hash10	user10@example.com	Отчество	Лебедев	Михаил	2
\.


--
-- TOC entry 5445 (class 0 OID 19015)
-- Dependencies: 291
-- Data for Name: пользователь_и_достижение; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."пользователь_и_достижение" ("пользователь_id", "достижение_id") FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
\.


--
-- TOC entry 5407 (class 0 OID 18926)
-- Dependencies: 253
-- Data for Name: приоритет_мышцы; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."приоритет_мышцы" (id, "название") FROM stdin;
1	Высокий
2	Низкий
3	Средний
\.


--
-- TOC entry 5413 (class 0 OID 18938)
-- Dependencies: 259
-- Data for Name: причина_чувства; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."причина_чувства" (id, "название") FROM stdin;
1	Усталость
2	Радость
3	Грусть
4	Счастье
5	Страх
6	Злость
7	Интерес
8	Спокойствие
9	Волнение
10	Удивление
\.


--
-- TOC entry 5389 (class 0 OID 18886)
-- Dependencies: 235
-- Data for Name: сложность_упражнения; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."сложность_упражнения" (id, "название") FROM stdin;
1	Легкая
2	Средняя
3	Тяжелая
\.


--
-- TOC entry 5385 (class 0 OID 18878)
-- Dependencies: 231
-- Data for Name: снаряжение; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."снаряжение" (id, "название") FROM stdin;
1	Гантели
2	Штанга
3	Беговая
4	Скакалка
5	Скамья
6	Мяч
7	Коврик
8	Резинка
9	Блок
10	Эспандер
\.


--
-- TOC entry 5403 (class 0 OID 18916)
-- Dependencies: 249
-- Data for Name: сообщение; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."сообщение" (id, "время_отправки", "текст") FROM stdin;
1	2025-03-05 13:30:29.523905+04	Сообщение 1
2	2025-03-05 13:30:29.523905+04	Сообщение 2
3	2025-03-05 13:30:29.523905+04	Сообщение 3
4	2025-03-05 13:30:29.523905+04	Сообщение 4
5	2025-03-05 13:30:29.523905+04	Сообщение 5
6	2025-03-05 13:30:29.523905+04	Сообщение 6
7	2025-03-05 13:30:29.523905+04	Сообщение 7
8	2025-03-05 13:30:29.523905+04	Сообщение 8
9	2025-03-05 13:30:29.523905+04	Сообщение 9
10	2025-03-05 13:30:29.523905+04	Сообщение 10
\.


--
-- TOC entry 5446 (class 0 OID 19018)
-- Dependencies: 292
-- Data for Name: сообщение_и_файл; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."сообщение_и_файл" ("сообщение_id", "файл_id") FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
\.


--
-- TOC entry 5381 (class 0 OID 18868)
-- Dependencies: 227
-- Data for Name: специальность_тренера; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."специальность_тренера" (id, "название") FROM stdin;
1	Фитнес
2	Бокс
3	Йога
4	Пилатес
5	Кроссфит
6	Стретчинг
7	Аэробика
8	Кардио
9	Силовые
10	Плавание
\.


--
-- TOC entry 5419 (class 0 OID 18950)
-- Dependencies: 265
-- Data for Name: статус_подписки; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."статус_подписки" (id, "название") FROM stdin;
1	Активна
2	Приостановлена
3	Завершена
\.


--
-- TOC entry 5435 (class 0 OID 18986)
-- Dependencies: 281
-- Data for Name: тип_тренировки; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."тип_тренировки" (id, "название") FROM stdin;
1	Кардио
2	Силовая
3	Йога
4	Пилатес
5	Аэробика
6	Функциональная
7	Стретчинг
8	Кроссфит
9	Танцы
10	Бокс
\.


--
-- TOC entry 5395 (class 0 OID 18900)
-- Dependencies: 241
-- Data for Name: тип_упражнения; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."тип_упражнения" (id, "название") FROM stdin;
1	Изолирующее
2	Составное
3	Комплексное
\.


--
-- TOC entry 5401 (class 0 OID 18912)
-- Dependencies: 247
-- Data for Name: тип_файла; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."тип_файла" (id, "название") FROM stdin;
1	Изображение
2	Видео
3	Документ
4	Аудио
\.


--
-- TOC entry 5379 (class 0 OID 18864)
-- Dependencies: 225
-- Data for Name: тренер; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."тренер" (id, "пользователь_id") FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
\.


--
-- TOC entry 5447 (class 0 OID 19021)
-- Dependencies: 293
-- Data for Name: тренер_и_клиент; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."тренер_и_клиент" ("тренер_id", "клиент_id") FROM stdin;
1	2
2	3
3	4
4	5
5	6
6	7
7	8
8	9
9	10
10	1
1	3
1	4
8	1
9	1
\.


--
-- TOC entry 5448 (class 0 OID 19024)
-- Dependencies: 294
-- Data for Name: тренер_и_специальность; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."тренер_и_специальность" ("тренер_id", "специальность_тренера_id") FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
\.


--
-- TOC entry 5431 (class 0 OID 18976)
-- Dependencies: 277
-- Data for Name: тренировка; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."тренировка" (id, "название", "является_онлайн", "время_начала", "чат_id") FROM stdin;
1	Тренировка 1	t	2023-04-01 14:00:00+04	1
2	Тренировка 2	f	2023-04-02 14:00:00+04	2
3	Тренировка 3	t	2023-04-03 14:00:00+04	3
4	Тренировка 4	f	2023-04-04 14:00:00+04	4
5	Тренировка 5	t	2023-04-05 14:00:00+04	5
6	Тренировка 6	f	2023-04-06 14:00:00+04	6
7	Тренировка 7	t	2023-04-07 14:00:00+04	7
8	Тренировка 8	f	2023-04-08 14:00:00+04	8
9	Тренировка 9	t	2023-04-09 14:00:00+04	9
10	Тренировка 10	f	2023-04-10 14:00:00+04	10
\.


--
-- TOC entry 5449 (class 0 OID 19027)
-- Dependencies: 295
-- Data for Name: тренировка_и_план_тренировки; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."тренировка_и_план_тренировки" ("тренировка_id", "план_тренировки_id") FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
2	1
\.


--
-- TOC entry 5450 (class 0 OID 19030)
-- Dependencies: 296
-- Data for Name: тренировка_и_пользователь; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."тренировка_и_пользователь" ("пользователь_id", "тренировка_id") FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
1	2
\.


--
-- TOC entry 5429 (class 0 OID 18972)
-- Dependencies: 275
-- Data for Name: тренировка_и_упражнение; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."тренировка_и_упражнение" (id, "тренировка_id", "упражнение_id", "номер_в_очереди", "колво_подходов", "колво_подходов_выполнено", "колво_повторений", "колво_повторений_выполнено", "этап_упражнения_id") FROM stdin;
1	1	1	1	3	3	10	10	1
2	2	2	2	3	3	10	10	2
3	3	3	3	3	3	10	10	3
4	4	4	4	3	3	10	10	1
5	5	5	5	3	3	10	10	2
6	6	6	6	3	3	10	10	3
7	7	7	7	3	3	10	10	1
8	8	8	8	3	3	10	10	2
9	9	9	9	3	3	10	10	3
10	10	10	10	3	3	10	10	1
\.


--
-- TOC entry 5391 (class 0 OID 18890)
-- Dependencies: 237
-- Data for Name: упражнение; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."упражнение" (id, "название", "описание", "тип_упражнения_id", "сложность_упражнения_id") FROM stdin;
1	Упражнение 1	Описание 1	1	1
2	Упражнение 2	Описание 2	2	2
3	Упражнение 3	Описание 3	3	3
4	Упражнение 4	Описание 4	1	1
5	Упражнение 5	Описание 5	2	2
6	Упражнение 6	Описание 6	3	3
7	Упражнение 7	Описание 7	1	1
8	Упражнение 8	Описание 8	2	2
9	Упражнение 9	Описание 9	3	3
10	Упражнение 10	Описание 10	1	1
\.


--
-- TOC entry 5387 (class 0 OID 18882)
-- Dependencies: 233
-- Data for Name: упражнение_и_мыщца; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."упражнение_и_мыщца" ("упражнение_id", "мышца_id", id, "приоритет_мышцы_id") FROM stdin;
1	1	1	1
2	2	2	2
3	3	3	3
4	4	4	1
5	5	5	2
6	6	6	3
7	7	7	1
8	8	8	2
9	9	9	3
10	10	10	1
\.


--
-- TOC entry 5451 (class 0 OID 19033)
-- Dependencies: 297
-- Data for Name: упражнение_и_пользователь; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."упражнение_и_пользователь" ("упражнение_id", "пользователь_id") FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
2	1
\.


--
-- TOC entry 5452 (class 0 OID 19036)
-- Dependencies: 298
-- Data for Name: упражнение_и_снаряжение; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."упражнение_и_снаряжение" ("упражнение_id", "снаряжение_id") FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
\.


--
-- TOC entry 5453 (class 0 OID 19039)
-- Dependencies: 299
-- Data for Name: упражнение_и_файл; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."упражнение_и_файл" ("упражнение_id", "файл_id") FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
\.


--
-- TOC entry 5454 (class 0 OID 19042)
-- Dependencies: 300
-- Data for Name: уровень_подготовки; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."уровень_подготовки" (id, "название") FROM stdin;
1	Новичок
2	Любитель
3	Профессионал
\.


--
-- TOC entry 5421 (class 0 OID 18954)
-- Dependencies: 267
-- Data for Name: уровень_тренировки; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."уровень_тренировки" (id, "название") FROM stdin;
1	Начальный
2	Средний
3	Продвинутый
10	Эксперт
\.


--
-- TOC entry 5399 (class 0 OID 18908)
-- Dependencies: 245
-- Data for Name: файл; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."файл" (id, "имя_файла") FROM stdin;
1	file1.jpg
2	file2.jpg
3	file3.jpg
4	file4.jpg
5	file5.jpg
6	file6.jpg
7	file7.jpg
8	file8.jpg
9	file9.jpg
10	file10.jpg
\.


--
-- TOC entry 5456 (class 0 OID 19047)
-- Dependencies: 302
-- Data for Name: файл_и_тип_файла; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."файл_и_тип_файла" ("файл_id", "тип_файла_id") FROM stdin;
1	1
2	2
3	3
4	1
5	2
6	3
7	1
8	2
9	3
10	1
\.


--
-- TOC entry 5411 (class 0 OID 18934)
-- Dependencies: 257
-- Data for Name: цель_тренировок; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."цель_тренировок" (id, "название") FROM stdin;
1	Похудение
2	Набор массы
3	Поддержка формы
4	Выносливость
5	Сила
6	Гибкость
7	Рельеф
8	Баланс
9	Здоровье
10	Эстетика
\.


--
-- TOC entry 5373 (class 0 OID 18852)
-- Dependencies: 219
-- Data for Name: чат; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."чат" (id) FROM stdin;
1
2
3
4
5
6
7
8
9
10
\.


--
-- TOC entry 5457 (class 0 OID 19050)
-- Dependencies: 303
-- Data for Name: чат_и_пользователь; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."чат_и_пользователь" ("пользователь_id", "чат_id") FROM stdin;
1	1
2	2
3	3
4	4
5	5
6	6
7	7
8	8
9	9
10	10
\.


--
-- TOC entry 5397 (class 0 OID 18904)
-- Dependencies: 243
-- Data for Name: чувство; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."чувство" (id, "название") FROM stdin;
1	Радость
2	Грусть
3	Удивление
4	Страх
5	Злость
6	Удовольствие
7	Спокойствие
8	Интерес
9	Восторг
10	Скука
\.


--
-- TOC entry 5415 (class 0 OID 18942)
-- Dependencies: 261
-- Data for Name: шаги; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."шаги" (id, "колво", "целевое_колво", "дата", "пользователь_id") FROM stdin;
1	10	15	2023-05-01	1
2	20	25	2023-05-02	2
3	30	35	2023-05-03	3
4	40	45	2023-05-04	4
5	50	55	2023-05-05	5
6	60	65	2023-05-06	6
7	70	75	2023-05-07	7
8	80	85	2023-05-08	8
10	100	105	2023-05-10	10
9	90	95	2023-05-09	1
\.


--
-- TOC entry 5393 (class 0 OID 18896)
-- Dependencies: 239
-- Data for Name: этап_упражнения; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."этап_упражнения" (id, "название") FROM stdin;
1	Разминка
2	Основной
3	Заминка
\.


--
-- TOC entry 5498 (class 0 OID 0)
-- Dependencies: 218
-- Name: achievements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.achievements_id_seq', 1, false);


--
-- TOC entry 5499 (class 0 OID 0)
-- Dependencies: 220
-- Name: chat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.chat_id_seq', 1, false);


--
-- TOC entry 5500 (class 0 OID 0)
-- Dependencies: 222
-- Name: client_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.client_id_seq', 1, false);


--
-- TOC entry 5501 (class 0 OID 0)
-- Dependencies: 224
-- Name: client_subscription_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.client_subscription_id_seq', 1, false);


--
-- TOC entry 5502 (class 0 OID 0)
-- Dependencies: 226
-- Name: coach_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.coach_id_seq', 1, false);


--
-- TOC entry 5503 (class 0 OID 0)
-- Dependencies: 228
-- Name: coach_speciality_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.coach_speciality_id_seq', 1, false);


--
-- TOC entry 5504 (class 0 OID 0)
-- Dependencies: 230
-- Name: diary_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.diary_id_seq', 21, true);


--
-- TOC entry 5505 (class 0 OID 0)
-- Dependencies: 232
-- Name: equipment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.equipment_id_seq', 1, false);


--
-- TOC entry 5506 (class 0 OID 0)
-- Dependencies: 234
-- Name: exercise_and_muscle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.exercise_and_muscle_id_seq', 1, false);


--
-- TOC entry 5507 (class 0 OID 0)
-- Dependencies: 236
-- Name: exercise_difficulty_2_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.exercise_difficulty_2_id_seq', 1, false);


--
-- TOC entry 5508 (class 0 OID 0)
-- Dependencies: 238
-- Name: exercise_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.exercise_id_seq', 1, false);


--
-- TOC entry 5509 (class 0 OID 0)
-- Dependencies: 240
-- Name: exercise_stage_2_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.exercise_stage_2_id_seq', 1, false);


--
-- TOC entry 5510 (class 0 OID 0)
-- Dependencies: 242
-- Name: exercise_type_2_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.exercise_type_2_id_seq', 1, false);


--
-- TOC entry 5511 (class 0 OID 0)
-- Dependencies: 244
-- Name: feeling_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.feeling_id_seq', 1, false);


--
-- TOC entry 5512 (class 0 OID 0)
-- Dependencies: 246
-- Name: file_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.file_id_seq', 1, false);


--
-- TOC entry 5513 (class 0 OID 0)
-- Dependencies: 248
-- Name: file_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.file_type_id_seq', 1, false);


--
-- TOC entry 5514 (class 0 OID 0)
-- Dependencies: 250
-- Name: message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.message_id_seq', 1, false);


--
-- TOC entry 5515 (class 0 OID 0)
-- Dependencies: 252
-- Name: muscle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.muscle_id_seq', 1, false);


--
-- TOC entry 5516 (class 0 OID 0)
-- Dependencies: 254
-- Name: muscle_priority_2_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.muscle_priority_2_id_seq', 1, false);


--
-- TOC entry 5517 (class 0 OID 0)
-- Dependencies: 256
-- Name: nutrition_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.nutrition_id_seq', 1, false);


--
-- TOC entry 5518 (class 0 OID 0)
-- Dependencies: 258
-- Name: purpose_of_workouts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.purpose_of_workouts_id_seq', 1, false);


--
-- TOC entry 5519 (class 0 OID 0)
-- Dependencies: 260
-- Name: reason_of_feeling_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reason_of_feeling_id_seq', 1, false);


--
-- TOC entry 5520 (class 0 OID 0)
-- Dependencies: 262
-- Name: steps_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.steps_id_seq', 1, false);


--
-- TOC entry 5521 (class 0 OID 0)
-- Dependencies: 264
-- Name: subscription_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subscription_id_seq', 1, false);


--
-- TOC entry 5522 (class 0 OID 0)
-- Dependencies: 266
-- Name: subscription_status_2_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subscription_status_2_id_seq', 1, false);


--
-- TOC entry 5523 (class 0 OID 0)
-- Dependencies: 268
-- Name: training_level_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.training_level_id_seq', 1, false);


--
-- TOC entry 5524 (class 0 OID 0)
-- Dependencies: 270
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 1, false);


--
-- TOC entry 5525 (class 0 OID 0)
-- Dependencies: 272
-- Name: water_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.water_id_seq', 1, false);


--
-- TOC entry 5526 (class 0 OID 0)
-- Dependencies: 274
-- Name: weight_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.weight_id_seq', 1, false);


--
-- TOC entry 5527 (class 0 OID 0)
-- Dependencies: 276
-- Name: workout_and_exercise_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.workout_and_exercise_id_seq', 1, false);


--
-- TOC entry 5528 (class 0 OID 0)
-- Dependencies: 278
-- Name: workout_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.workout_id_seq', 1, false);


--
-- TOC entry 5529 (class 0 OID 0)
-- Dependencies: 280
-- Name: workout_plan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.workout_plan_id_seq', 1, false);


--
-- TOC entry 5530 (class 0 OID 0)
-- Dependencies: 282
-- Name: workout_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.workout_type_id_seq', 1, false);


--
-- TOC entry 5531 (class 0 OID 0)
-- Dependencies: 286
-- Name: имя_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."имя_id_seq"', 1, false);


--
-- TOC entry 5532 (class 0 OID 0)
-- Dependencies: 301
-- Name: уровень_подготовки_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."уровень_подготовки_id_seq"', 1, false);


--
-- TOC entry 5031 (class 2606 OID 19089)
-- Name: достижение achievements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."достижение"
    ADD CONSTRAINT achievements_pkey PRIMARY KEY (id);


--
-- TOC entry 5169 (class 2606 OID 19091)
-- Name: чат_и_пользователь chat_id_user_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."чат_и_пользователь"
    ADD CONSTRAINT chat_id_user_id PRIMARY KEY ("пользователь_id", "чат_id") INCLUDE ("пользователь_id", "чат_id");


--
-- TOC entry 5033 (class 2606 OID 19093)
-- Name: чат chat_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."чат"
    ADD CONSTRAINT chat_pkey PRIMARY KEY (id);


--
-- TOC entry 4969 (class 2606 OID 19094)
-- Name: клиент_и_подписка chk_client_and_subscription_date_range; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."клиент_и_подписка"
    ADD CONSTRAINT chk_client_and_subscription_date_range CHECK (("дата_начала" < "дата_истечения")) NOT VALID;


--
-- TOC entry 4970 (class 2606 OID 19095)
-- Name: клиент_и_подписка chk_client_and_subscription_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."клиент_и_подписка"
    ADD CONSTRAINT chk_client_and_subscription_ids CHECK ((("клиент_id" >= 1) AND ("подписка_id" >= 1))) NOT VALID;


--
-- TOC entry 4971 (class 2606 OID 19096)
-- Name: клиент_и_подписка chk_client_and_subscription_pause_date; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."клиент_и_подписка"
    ADD CONSTRAINT chk_client_and_subscription_pause_date CHECK ((("дата_паузы" >= "дата_начала") AND ("дата_паузы" <= "дата_истечения"))) NOT VALID;


--
-- TOC entry 5013 (class 2606 OID 19097)
-- Name: клиент_и_тип_тренировки chk_client_and_workout_type_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."клиент_и_тип_тренировки"
    ADD CONSTRAINT chk_client_and_workout_type_ids CHECK ((("клиент_id" >= 1) AND ("тип_тренировки_id" >= 1))) NOT VALID;


--
-- TOC entry 5012 (class 2606 OID 19098)
-- Name: дневник_и_чувство chk_diary_and_feeling_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."дневник_и_чувство"
    ADD CONSTRAINT chk_diary_and_feeling_ids CHECK ((("дневник_id" >= 1) AND ("чувство_id" >= 1))) NOT VALID;


--
-- TOC entry 5011 (class 2606 OID 19099)
-- Name: дневник_и_причина_чувства chk_diary_and_feeling_reason_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."дневник_и_причина_чувства"
    ADD CONSTRAINT chk_diary_and_feeling_reason_ids CHECK ((("дневник_id" >= 1) AND ("причина_чувства_id" >= 1))) NOT VALID;


--
-- TOC entry 4975 (class 2606 OID 19100)
-- Name: снаряжение chk_equipment_name; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."снаряжение"
    ADD CONSTRAINT chk_equipment_name CHECK ((("название")::text ~ '^[А-Яа-яёЁ\s]+$'::text)) NOT VALID;


--
-- TOC entry 4977 (class 2606 OID 19101)
-- Name: сложность_упражнения chk_exercise_difficult; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."сложность_упражнения"
    ADD CONSTRAINT chk_exercise_difficult CHECK ((("название")::text ~ '^[А-Яа-яёЁ\s]+$'::text)) NOT VALID;


--
-- TOC entry 4979 (class 2606 OID 19102)
-- Name: этап_упражнения chk_exercise_stage_name; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."этап_упражнения"
    ADD CONSTRAINT chk_exercise_stage_name CHECK ((("название")::text ~ '^[А-Яа-яёЁ\s]+$'::text)) NOT VALID;


--
-- TOC entry 4980 (class 2606 OID 19103)
-- Name: тип_упражнения chk_exercise_type; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."тип_упражнения"
    ADD CONSTRAINT chk_exercise_type CHECK ((("название")::text ~ '^[А-Яа-яёЁ\s]+$'::text)) NOT VALID;


--
-- TOC entry 4981 (class 2606 OID 19104)
-- Name: чувство chk_feeling_name; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."чувство"
    ADD CONSTRAINT chk_feeling_name CHECK ((("название")::text ~ '^[А-Яа-яёЁ\s]+$'::text)) NOT VALID;


--
-- TOC entry 4991 (class 2606 OID 19105)
-- Name: причина_чувства chk_feeling_reason; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."причина_чувства"
    ADD CONSTRAINT chk_feeling_reason CHECK ((("название")::text ~ '^[А-Яа-яёЁ\s]+$'::text)) NOT VALID;


--
-- TOC entry 4982 (class 2606 OID 19106)
-- Name: тип_файла chk_file_type; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."тип_файла"
    ADD CONSTRAINT chk_file_type CHECK ((("название")::text ~ '^[А-Яа-яёЁ\s]+$'::text)) NOT VALID;


--
-- TOC entry 5014 (class 2606 OID 19107)
-- Name: клиент_и_цель_тренировок chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."клиент_и_цель_тренировок"
    ADD CONSTRAINT chk_ids CHECK ((("клиент_id" >= 1) AND ("цель_тренировок_id" >= 1))) NOT VALID;


--
-- TOC entry 5017 (class 2606 OID 19108)
-- Name: план_тренировки_и_пользователь chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."план_тренировки_и_пользователь"
    ADD CONSTRAINT chk_ids CHECK ((("пользователь_id" >= 1) AND ("план_тренировки_id" >= 1))) NOT VALID;


--
-- TOC entry 5018 (class 2606 OID 19109)
-- Name: пользователь_и_достижение chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."пользователь_и_достижение"
    ADD CONSTRAINT chk_ids CHECK ((("пользователь_id" >= 1) AND ("достижение_id" >= 1))) NOT VALID;


--
-- TOC entry 5019 (class 2606 OID 19110)
-- Name: сообщение_и_файл chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."сообщение_и_файл"
    ADD CONSTRAINT chk_ids CHECK ((("сообщение_id" >= 1) AND ("файл_id" >= 1))) NOT VALID;


--
-- TOC entry 5020 (class 2606 OID 19111)
-- Name: тренер_и_клиент chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."тренер_и_клиент"
    ADD CONSTRAINT chk_ids CHECK ((("тренер_id" >= 1) AND ("клиент_id" >= 1))) NOT VALID;


--
-- TOC entry 5021 (class 2606 OID 19112)
-- Name: тренер_и_специальность chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."тренер_и_специальность"
    ADD CONSTRAINT chk_ids CHECK ((("тренер_id" >= 1) AND ("специальность_тренера_id" >= 1))) NOT VALID;


--
-- TOC entry 5022 (class 2606 OID 19113)
-- Name: тренировка_и_план_тренировки chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."тренировка_и_план_тренировки"
    ADD CONSTRAINT chk_ids CHECK ((("тренировка_id" >= 1) AND ("план_тренировки_id" >= 1))) NOT VALID;


--
-- TOC entry 5023 (class 2606 OID 19114)
-- Name: тренировка_и_пользователь chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."тренировка_и_пользователь"
    ADD CONSTRAINT chk_ids CHECK ((("пользователь_id" >= 1) AND ("тренировка_id" >= 1))) NOT VALID;


--
-- TOC entry 5007 (class 2606 OID 19115)
-- Name: тренировка_и_упражнение chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."тренировка_и_упражнение"
    ADD CONSTRAINT chk_ids CHECK ((("тренировка_id" >= 1) AND ("упражнение_id" >= 1) AND ("этап_упражнения_id" >= 1))) NOT VALID;


--
-- TOC entry 4976 (class 2606 OID 19116)
-- Name: упражнение_и_мыщца chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."упражнение_и_мыщца"
    ADD CONSTRAINT chk_ids CHECK ((("упражнение_id" >= 1) AND ("мышца_id" >= 1) AND ("приоритет_мышцы_id" >= 1))) NOT VALID;


--
-- TOC entry 5024 (class 2606 OID 19117)
-- Name: упражнение_и_пользователь chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."упражнение_и_пользователь"
    ADD CONSTRAINT chk_ids CHECK ((("упражнение_id" >= 1) AND ("пользователь_id" >= 1))) NOT VALID;


--
-- TOC entry 5025 (class 2606 OID 19118)
-- Name: упражнение_и_снаряжение chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."упражнение_и_снаряжение"
    ADD CONSTRAINT chk_ids CHECK ((("упражнение_id" >= 1) AND ("снаряжение_id" >= 1))) NOT VALID;


--
-- TOC entry 5026 (class 2606 OID 19119)
-- Name: упражнение_и_файл chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."упражнение_и_файл"
    ADD CONSTRAINT chk_ids CHECK ((("упражнение_id" >= 1) AND ("файл_id" >= 1))) NOT VALID;


--
-- TOC entry 5028 (class 2606 OID 19120)
-- Name: файл_и_тип_файла chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."файл_и_тип_файла"
    ADD CONSTRAINT chk_ids CHECK ((("файл_id" >= 1) AND ("тип_файла_id" >= 1))) NOT VALID;


--
-- TOC entry 5029 (class 2606 OID 19121)
-- Name: чат_и_пользователь chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."чат_и_пользователь"
    ADD CONSTRAINT chk_ids CHECK ((("пользователь_id" >= 1) AND ("чат_id" >= 1))) NOT VALID;


--
-- TOC entry 4992 (class 2606 OID 19122)
-- Name: шаги chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."шаги"
    ADD CONSTRAINT chk_ids CHECK (("пользователь_id" >= 1)) NOT VALID;


--
-- TOC entry 5005 (class 2606 OID 19123)
-- Name: вес chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."вес"
    ADD CONSTRAINT chk_ids CHECK (("пользователь_id" >= 1)) NOT VALID;


--
-- TOC entry 5003 (class 2606 OID 19124)
-- Name: вода chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."вода"
    ADD CONSTRAINT chk_ids CHECK (("пользователь_id" >= 1)) NOT VALID;


--
-- TOC entry 4974 (class 2606 OID 19125)
-- Name: дневник chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."дневник"
    ADD CONSTRAINT chk_ids CHECK ((("пользователь_id" >= 1) AND ("файл_id" >= 1))) NOT VALID;


--
-- TOC entry 4968 (class 2606 OID 19126)
-- Name: клиент chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."клиент"
    ADD CONSTRAINT chk_ids CHECK ((("уровень_подготовки_id" >= 1) AND ("пользователь_id" >= 1))) NOT VALID;


--
-- TOC entry 5015 (class 2606 OID 19127)
-- Name: отзыв chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."отзыв"
    ADD CONSTRAINT chk_ids CHECK ((("клиент_id" >= 1) AND ("тренер_id" >= 1))) NOT VALID;


--
-- TOC entry 4985 (class 2606 OID 19128)
-- Name: питание chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."питание"
    ADD CONSTRAINT chk_ids CHECK (("пользователь_id" >= 1)) NOT VALID;


--
-- TOC entry 4998 (class 2606 OID 19129)
-- Name: пользователь chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."пользователь"
    ADD CONSTRAINT chk_ids CHECK (("пол_id" >= 1)) NOT VALID;


--
-- TOC entry 4972 (class 2606 OID 19130)
-- Name: тренер chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."тренер"
    ADD CONSTRAINT chk_ids CHECK (("пользователь_id" >= 1)) NOT VALID;


--
-- TOC entry 5009 (class 2606 OID 19131)
-- Name: тренировка chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."тренировка"
    ADD CONSTRAINT chk_ids CHECK (("чат_id" >= 1)) NOT VALID;


--
-- TOC entry 4978 (class 2606 OID 19132)
-- Name: упражнение chk_ids; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."упражнение"
    ADD CONSTRAINT chk_ids CHECK ((("тип_упражнения_id" >= 1) AND ("сложность_упражнения_id" >= 1))) NOT VALID;


--
-- TOC entry 5008 (class 2606 OID 19133)
-- Name: тренировка_и_упражнение chk_more_or_equal_one; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."тренировка_и_упражнение"
    ADD CONSTRAINT chk_more_or_equal_one CHECK ((("номер_в_очереди" >= 0) AND ("колво_подходов" >= 1) AND (("колво_подходов_выполнено" >= 1) AND ("колво_подходов_выполнено" <= "колво_подходов")) AND ("колво_повторений" >= 1) AND (("колво_повторений_выполнено" >= 1) AND ("колво_повторений_выполнено" <= "колво_повторений")))) NOT VALID;


--
-- TOC entry 4993 (class 2606 OID 19134)
-- Name: шаги chk_more_or_equal_one; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."шаги"
    ADD CONSTRAINT chk_more_or_equal_one CHECK ((("колво" >= 0) AND ("целевое_колво" >= 0))) NOT VALID;


--
-- TOC entry 4983 (class 2606 OID 19135)
-- Name: мышца chk_muscle_name; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."мышца"
    ADD CONSTRAINT chk_muscle_name CHECK ((("название")::text ~ '^[А-Яа-яёЁ\s]+$'::text)) NOT VALID;


--
-- TOC entry 4984 (class 2606 OID 19136)
-- Name: приоритет_мышцы chk_muscle_priority; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."приоритет_мышцы"
    ADD CONSTRAINT chk_muscle_priority CHECK ((("название")::text ~ '^[А-Яа-яёЁ\s]+$'::text)) NOT VALID;


--
-- TOC entry 4986 (class 2606 OID 19137)
-- Name: питание chk_nutrition_calories; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."питание"
    ADD CONSTRAINT chk_nutrition_calories CHECK ((("калории" >= 0) AND ("калории" <= 15000))) NOT VALID;


--
-- TOC entry 4987 (class 2606 OID 19138)
-- Name: питание chk_nutrition_carbohydrates; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."питание"
    ADD CONSTRAINT chk_nutrition_carbohydrates CHECK ((("углеводы" >= 0) AND ("углеводы" <= 2000))) NOT VALID;


--
-- TOC entry 4988 (class 2606 OID 19139)
-- Name: питание chk_nutrition_fats; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."питание"
    ADD CONSTRAINT chk_nutrition_fats CHECK ((("жиры" >= 0) AND ("жиры" <= 1000))) NOT VALID;


--
-- TOC entry 4989 (class 2606 OID 19140)
-- Name: питание chk_nutrition_proteins; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."питание"
    ADD CONSTRAINT chk_nutrition_proteins CHECK ((("белки" >= 0) AND ("белки" <= 2000))) NOT VALID;


--
-- TOC entry 4994 (class 2606 OID 19141)
-- Name: подписка chk_subscription_price; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."подписка"
    ADD CONSTRAINT chk_subscription_price CHECK ((("цена" >= 0) AND ("цена" <= 10000000))) NOT VALID;


--
-- TOC entry 4996 (class 2606 OID 19142)
-- Name: статус_подписки chk_subscription_status; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."статус_подписки"
    ADD CONSTRAINT chk_subscription_status CHECK ((("название")::text ~ '^[А-Яа-яёЁ\s]+$'::text)) NOT VALID;


--
-- TOC entry 4995 (class 2606 OID 19143)
-- Name: подписка chk_subscription_validity_period; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."подписка"
    ADD CONSTRAINT chk_subscription_validity_period CHECK (("срок_действия" >= 0)) NOT VALID;


--
-- TOC entry 4999 (class 2606 OID 19144)
-- Name: пользователь chk_user_email; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."пользователь"
    ADD CONSTRAINT chk_user_email CHECK ((("почта")::text ~* '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'::text)) NOT VALID;


--
-- TOC entry 5000 (class 2606 OID 19145)
-- Name: пользователь chk_user_name; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."пользователь"
    ADD CONSTRAINT chk_user_name CHECK ((("имя")::text ~ '^[А-Яа-яёЁ]+$'::text)) NOT VALID;


--
-- TOC entry 5001 (class 2606 OID 19146)
-- Name: пользователь chk_user_patronymic; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."пользователь"
    ADD CONSTRAINT chk_user_patronymic CHECK ((("отчество")::text ~ '^[А-Яа-яёЁ]+$'::text)) NOT VALID;


--
-- TOC entry 5002 (class 2606 OID 19147)
-- Name: пользователь chk_user_surname; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."пользователь"
    ADD CONSTRAINT chk_user_surname CHECK ((("фамилия")::text ~ '^[А-Яа-яёЁ]+$'::text)) NOT VALID;


--
-- TOC entry 5004 (class 2606 OID 19148)
-- Name: вода chk_volume; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."вода"
    ADD CONSTRAINT chk_volume CHECK ((("объем" >= 0) AND ("объем" <= 10000) AND (("целевой_объем" >= 0) AND ("целевой_объем" <= 10000)))) NOT VALID;


--
-- TOC entry 5006 (class 2606 OID 19149)
-- Name: вес chk_weight; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."вес"
    ADD CONSTRAINT chk_weight CHECK ((("вес" >= 0) AND ("вес" <= 300))) NOT VALID;


--
-- TOC entry 4997 (class 2606 OID 19150)
-- Name: уровень_тренировки chk_workout_level_name; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."уровень_тренировки"
    ADD CONSTRAINT chk_workout_level_name CHECK ((("название")::text ~ '^[А-Яа-яёЁ\s]+$'::text)) NOT VALID;


--
-- TOC entry 4990 (class 2606 OID 19151)
-- Name: цель_тренировок chk_workout_target_name; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."цель_тренировок"
    ADD CONSTRAINT chk_workout_target_name CHECK ((("название")::text ~ '^[А-Яа-яёЁ\s]+$'::text)) NOT VALID;


--
-- TOC entry 5010 (class 2606 OID 19152)
-- Name: тип_тренировки chk_workout_type_name; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."тип_тренировки"
    ADD CONSTRAINT chk_workout_type_name CHECK ((("название")::text ~ '^[А-Яа-яёЁ\s]+$'::text)) NOT VALID;


--
-- TOC entry 5139 (class 2606 OID 19154)
-- Name: клиент_и_цель_тренировок client_id_purpose_of_workouts_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."клиент_и_цель_тренировок"
    ADD CONSTRAINT client_id_purpose_of_workouts_id PRIMARY KEY ("клиент_id", "цель_тренировок_id") INCLUDE ("клиент_id", "цель_тренировок_id");


--
-- TOC entry 5137 (class 2606 OID 19156)
-- Name: клиент_и_тип_тренировки client_id_workout_type_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."клиент_и_тип_тренировки"
    ADD CONSTRAINT client_id_workout_type_id PRIMARY KEY ("клиент_id", "тип_тренировки_id") INCLUDE ("клиент_id", "тип_тренировки_id");


--
-- TOC entry 5035 (class 2606 OID 19158)
-- Name: клиент client_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."клиент"
    ADD CONSTRAINT client_pkey PRIMARY KEY (id);


--
-- TOC entry 5037 (class 2606 OID 19160)
-- Name: клиент_и_подписка client_subscription_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."клиент_и_подписка"
    ADD CONSTRAINT client_subscription_pkey PRIMARY KEY (id);


--
-- TOC entry 5149 (class 2606 OID 19162)
-- Name: тренер_и_клиент coach_id_client_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренер_и_клиент"
    ADD CONSTRAINT coach_id_client_id PRIMARY KEY ("тренер_id", "клиент_id") INCLUDE ("тренер_id", "клиент_id");


--
-- TOC entry 5151 (class 2606 OID 19164)
-- Name: тренер_и_специальность coach_id_speciality_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренер_и_специальность"
    ADD CONSTRAINT coach_id_speciality_id PRIMARY KEY ("тренер_id", "специальность_тренера_id") INCLUDE ("тренер_id", "специальность_тренера_id");


--
-- TOC entry 5039 (class 2606 OID 19166)
-- Name: тренер coach_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренер"
    ADD CONSTRAINT coach_pkey PRIMARY KEY (id);


--
-- TOC entry 4973 (class 2606 OID 19167)
-- Name: специальность_тренера coach_speciality; Type: CHECK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE public."специальность_тренера"
    ADD CONSTRAINT coach_speciality CHECK ((("название")::text ~ '^[А-Яа-яёЁ\s]+$'::text)) NOT VALID;


--
-- TOC entry 5043 (class 2606 OID 19169)
-- Name: специальность_тренера coach_speciality_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."специальность_тренера"
    ADD CONSTRAINT coach_speciality_pkey PRIMARY KEY (id);


--
-- TOC entry 5041 (class 2606 OID 19171)
-- Name: тренер coach_user_id_uq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренер"
    ADD CONSTRAINT coach_user_id_uq UNIQUE ("пользователь_id") INCLUDE ("пользователь_id");


--
-- TOC entry 5131 (class 2606 OID 19173)
-- Name: дневник_и_чувство diary_and_feeling_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."дневник_и_чувство"
    ADD CONSTRAINT diary_and_feeling_pkey PRIMARY KEY ("дневник_id", "чувство_id");


--
-- TOC entry 5129 (class 2606 OID 19175)
-- Name: дневник_и_причина_чувства diary_and_reason_of_feeling_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."дневник_и_причина_чувства"
    ADD CONSTRAINT diary_and_reason_of_feeling_pkey PRIMARY KEY ("дневник_id", "причина_чувства_id");


--
-- TOC entry 5047 (class 2606 OID 19177)
-- Name: дневник diary_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."дневник"
    ADD CONSTRAINT diary_pkey PRIMARY KEY (id);


--
-- TOC entry 5049 (class 2606 OID 19179)
-- Name: снаряжение equipment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."снаряжение"
    ADD CONSTRAINT equipment_pkey PRIMARY KEY (id);


--
-- TOC entry 5159 (class 2606 OID 19181)
-- Name: упражнение_и_снаряжение exercise_and_equipment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."упражнение_и_снаряжение"
    ADD CONSTRAINT exercise_and_equipment_pkey PRIMARY KEY ("упражнение_id", "снаряжение_id");


--
-- TOC entry 5161 (class 2606 OID 19183)
-- Name: упражнение_и_файл exercise_and_file_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."упражнение_и_файл"
    ADD CONSTRAINT exercise_and_file_pkey PRIMARY KEY ("упражнение_id", "файл_id");


--
-- TOC entry 5053 (class 2606 OID 19185)
-- Name: упражнение_и_мыщца exercise_and_muscle_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."упражнение_и_мыщца"
    ADD CONSTRAINT exercise_and_muscle_pkey PRIMARY KEY (id);


--
-- TOC entry 5055 (class 2606 OID 19187)
-- Name: сложность_упражнения exercise_difficulty_2_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."сложность_упражнения"
    ADD CONSTRAINT exercise_difficulty_2_pkey PRIMARY KEY (id);


--
-- TOC entry 5157 (class 2606 OID 19189)
-- Name: упражнение_и_пользователь exercise_id_user_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."упражнение_и_пользователь"
    ADD CONSTRAINT exercise_id_user_id PRIMARY KEY ("упражнение_id", "пользователь_id") INCLUDE ("упражнение_id", "пользователь_id");


--
-- TOC entry 5059 (class 2606 OID 19191)
-- Name: упражнение exercise_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."упражнение"
    ADD CONSTRAINT exercise_pkey PRIMARY KEY (id);


--
-- TOC entry 5061 (class 2606 OID 19193)
-- Name: этап_упражнения exercise_stage_2_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."этап_упражнения"
    ADD CONSTRAINT exercise_stage_2_pkey PRIMARY KEY (id);


--
-- TOC entry 5065 (class 2606 OID 19195)
-- Name: тип_упражнения exercise_type_2_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тип_упражнения"
    ADD CONSTRAINT exercise_type_2_pkey PRIMARY KEY (id);


--
-- TOC entry 5141 (class 2606 OID 19197)
-- Name: отзыв feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."отзыв"
    ADD CONSTRAINT feedback_pkey PRIMARY KEY ("клиент_id", "тренер_id");


--
-- TOC entry 5069 (class 2606 OID 19199)
-- Name: чувство feeling_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."чувство"
    ADD CONSTRAINT feeling_pkey PRIMARY KEY (id);


--
-- TOC entry 5167 (class 2606 OID 19201)
-- Name: файл_и_тип_файла file_and_file_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."файл_и_тип_файла"
    ADD CONSTRAINT file_and_file_type_pkey PRIMARY KEY ("файл_id", "тип_файла_id");


--
-- TOC entry 5073 (class 2606 OID 19203)
-- Name: файл file_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."файл"
    ADD CONSTRAINT file_pkey PRIMARY KEY (id);


--
-- TOC entry 5075 (class 2606 OID 19205)
-- Name: тип_файла file_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тип_файла"
    ADD CONSTRAINT file_type_pkey PRIMARY KEY (id);


--
-- TOC entry 5147 (class 2606 OID 19207)
-- Name: сообщение_и_файл message_and_file_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."сообщение_и_файл"
    ADD CONSTRAINT message_and_file_pkey PRIMARY KEY ("сообщение_id", "файл_id");


--
-- TOC entry 5079 (class 2606 OID 19209)
-- Name: сообщение message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."сообщение"
    ADD CONSTRAINT message_pkey PRIMARY KEY (id);


--
-- TOC entry 5081 (class 2606 OID 19211)
-- Name: мышца muscle_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."мышца"
    ADD CONSTRAINT muscle_pkey PRIMARY KEY (id);


--
-- TOC entry 5085 (class 2606 OID 19213)
-- Name: приоритет_мышцы muscle_priority_2_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."приоритет_мышцы"
    ADD CONSTRAINT muscle_priority_2_pkey PRIMARY KEY (id);


--
-- TOC entry 5089 (class 2606 OID 19215)
-- Name: питание nutrition_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."питание"
    ADD CONSTRAINT nutrition_pkey PRIMARY KEY (id);


--
-- TOC entry 5091 (class 2606 OID 19217)
-- Name: цель_тренировок purpose_of_workouts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."цель_тренировок"
    ADD CONSTRAINT purpose_of_workouts_pkey PRIMARY KEY (id);


--
-- TOC entry 5095 (class 2606 OID 19219)
-- Name: причина_чувства reason_of_feeling_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."причина_чувства"
    ADD CONSTRAINT reason_of_feeling_pkey PRIMARY KEY (id);


--
-- TOC entry 5099 (class 2606 OID 19221)
-- Name: шаги steps_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."шаги"
    ADD CONSTRAINT steps_pkey PRIMARY KEY (id);


--
-- TOC entry 5101 (class 2606 OID 19223)
-- Name: подписка subscription_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."подписка"
    ADD CONSTRAINT subscription_pkey PRIMARY KEY (id);


--
-- TOC entry 5105 (class 2606 OID 19225)
-- Name: статус_подписки subscription_status_2_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."статус_подписки"
    ADD CONSTRAINT subscription_status_2_pkey PRIMARY KEY (id);


--
-- TOC entry 5109 (class 2606 OID 19227)
-- Name: уровень_тренировки training_level_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."уровень_тренировки"
    ADD CONSTRAINT training_level_pkey PRIMARY KEY (id);


--
-- TOC entry 5045 (class 2606 OID 19229)
-- Name: специальность_тренера unique_coach_speciality_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."специальность_тренера"
    ADD CONSTRAINT unique_coach_speciality_name UNIQUE ("название");


--
-- TOC entry 5051 (class 2606 OID 19231)
-- Name: снаряжение unique_equipment_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."снаряжение"
    ADD CONSTRAINT unique_equipment_name UNIQUE ("название");


--
-- TOC entry 5057 (class 2606 OID 19233)
-- Name: сложность_упражнения unique_exercise_difficulty_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."сложность_упражнения"
    ADD CONSTRAINT unique_exercise_difficulty_name UNIQUE ("название");


--
-- TOC entry 5063 (class 2606 OID 19235)
-- Name: этап_упражнения unique_exercise_stage_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."этап_упражнения"
    ADD CONSTRAINT unique_exercise_stage_name UNIQUE ("название");


--
-- TOC entry 5067 (class 2606 OID 19237)
-- Name: тип_упражнения unique_exercise_type_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тип_упражнения"
    ADD CONSTRAINT unique_exercise_type_name UNIQUE ("название");


--
-- TOC entry 5071 (class 2606 OID 19239)
-- Name: чувство unique_feeling_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."чувство"
    ADD CONSTRAINT unique_feeling_name UNIQUE ("название");


--
-- TOC entry 5097 (class 2606 OID 19241)
-- Name: причина_чувства unique_feeling_reason_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."причина_чувства"
    ADD CONSTRAINT unique_feeling_reason_name UNIQUE ("название");


--
-- TOC entry 5077 (class 2606 OID 19243)
-- Name: тип_файла unique_file_type_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тип_файла"
    ADD CONSTRAINT unique_file_type_name UNIQUE ("название");


--
-- TOC entry 5083 (class 2606 OID 19245)
-- Name: мышца unique_muscle_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."мышца"
    ADD CONSTRAINT unique_muscle_name UNIQUE ("название");


--
-- TOC entry 5087 (class 2606 OID 19247)
-- Name: приоритет_мышцы unique_muscle_priority_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."приоритет_мышцы"
    ADD CONSTRAINT unique_muscle_priority_name UNIQUE ("название");


--
-- TOC entry 5163 (class 2606 OID 19249)
-- Name: уровень_подготовки unique_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."уровень_подготовки"
    ADD CONSTRAINT unique_name UNIQUE ("название");


--
-- TOC entry 5133 (class 2606 OID 19251)
-- Name: пол unique_sex_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."пол"
    ADD CONSTRAINT unique_sex_name UNIQUE ("название");


--
-- TOC entry 5103 (class 2606 OID 19253)
-- Name: подписка unique_subscription_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."подписка"
    ADD CONSTRAINT unique_subscription_name UNIQUE ("название");


--
-- TOC entry 5107 (class 2606 OID 19255)
-- Name: статус_подписки unique_subscription_status_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."статус_подписки"
    ADD CONSTRAINT unique_subscription_status_name UNIQUE ("название");


--
-- TOC entry 5111 (class 2606 OID 19257)
-- Name: пользователь unique_user_mail; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."пользователь"
    ADD CONSTRAINT unique_user_mail UNIQUE ("почта");


--
-- TOC entry 5125 (class 2606 OID 19259)
-- Name: тип_тренировки unique_workout_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тип_тренировки"
    ADD CONSTRAINT unique_workout_name UNIQUE ("название");


--
-- TOC entry 5093 (class 2606 OID 19261)
-- Name: цель_тренировок unique_workout_target_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."цель_тренировок"
    ADD CONSTRAINT unique_workout_target_name UNIQUE ("название");


--
-- TOC entry 5145 (class 2606 OID 19263)
-- Name: пользователь_и_достижение user_and_achievment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."пользователь_и_достижение"
    ADD CONSTRAINT user_and_achievment_pkey PRIMARY KEY ("пользователь_id", "достижение_id");


--
-- TOC entry 5113 (class 2606 OID 19265)
-- Name: пользователь user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."пользователь"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 5115 (class 2606 OID 19267)
-- Name: вода water_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."вода"
    ADD CONSTRAINT water_pkey PRIMARY KEY (id);


--
-- TOC entry 5117 (class 2606 OID 19269)
-- Name: вес weight_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."вес"
    ADD CONSTRAINT weight_pkey PRIMARY KEY (id);


--
-- TOC entry 5119 (class 2606 OID 19271)
-- Name: тренировка_и_упражнение workout_and_exercise_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренировка_и_упражнение"
    ADD CONSTRAINT workout_and_exercise_pkey PRIMARY KEY (id);


--
-- TOC entry 5153 (class 2606 OID 19273)
-- Name: тренировка_и_план_тренировки workout_and_workout_plan_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренировка_и_план_тренировки"
    ADD CONSTRAINT workout_and_workout_plan_pkey PRIMARY KEY ("тренировка_id", "план_тренировки_id");


--
-- TOC entry 5155 (class 2606 OID 19275)
-- Name: тренировка_и_пользователь workout_id_user_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренировка_и_пользователь"
    ADD CONSTRAINT workout_id_user_id PRIMARY KEY ("пользователь_id", "тренировка_id");


--
-- TOC entry 5121 (class 2606 OID 19277)
-- Name: тренировка workout_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренировка"
    ADD CONSTRAINT workout_pkey PRIMARY KEY (id);


--
-- TOC entry 5143 (class 2606 OID 19279)
-- Name: план_тренировки_и_пользователь workout_plan_id_user_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."план_тренировки_и_пользователь"
    ADD CONSTRAINT workout_plan_id_user_id PRIMARY KEY ("пользователь_id", "план_тренировки_id") INCLUDE ("пользователь_id", "план_тренировки_id");


--
-- TOC entry 5123 (class 2606 OID 19281)
-- Name: план_тренировки workout_plan_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."план_тренировки"
    ADD CONSTRAINT workout_plan_pkey PRIMARY KEY (id);


--
-- TOC entry 5127 (class 2606 OID 19283)
-- Name: тип_тренировки workout_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тип_тренировки"
    ADD CONSTRAINT workout_type_pkey PRIMARY KEY (id);


--
-- TOC entry 5135 (class 2606 OID 19285)
-- Name: пол имя_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."пол"
    ADD CONSTRAINT "имя_pkey" PRIMARY KEY (id);


--
-- TOC entry 5165 (class 2606 OID 19287)
-- Name: уровень_подготовки уровень_подготовки_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."уровень_подготовки"
    ADD CONSTRAINT "уровень_подготовки_pkey" PRIMARY KEY (id);


--
-- TOC entry 5224 (class 2606 OID 19288)
-- Name: чат_и_пользователь chat_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."чат_и_пользователь"
    ADD CONSTRAINT chat_id FOREIGN KEY ("чат_id") REFERENCES public."чат"(id);


--
-- TOC entry 5191 (class 2606 OID 19293)
-- Name: тренировка chat_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренировка"
    ADD CONSTRAINT chat_id FOREIGN KEY ("чат_id") REFERENCES public."чат"(id) NOT VALID;


--
-- TOC entry 5172 (class 2606 OID 19298)
-- Name: клиент_и_подписка client_and_subscription_subscription_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."клиент_и_подписка"
    ADD CONSTRAINT client_and_subscription_subscription_status_id_fkey FOREIGN KEY ("статус_подписки_id") REFERENCES public."статус_подписки"(id) NOT VALID;


--
-- TOC entry 5208 (class 2606 OID 19303)
-- Name: тренер_и_клиент client_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренер_и_клиент"
    ADD CONSTRAINT client_id FOREIGN KEY ("клиент_id") REFERENCES public."клиент"(id);


--
-- TOC entry 5198 (class 2606 OID 19308)
-- Name: клиент_и_цель_тренировок client_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."клиент_и_цель_тренировок"
    ADD CONSTRAINT client_id FOREIGN KEY ("клиент_id") REFERENCES public."клиент"(id);


--
-- TOC entry 5196 (class 2606 OID 19313)
-- Name: клиент_и_тип_тренировки client_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."клиент_и_тип_тренировки"
    ADD CONSTRAINT client_id FOREIGN KEY ("клиент_id") REFERENCES public."клиент"(id);


--
-- TOC entry 5173 (class 2606 OID 19318)
-- Name: клиент_и_подписка client_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."клиент_и_подписка"
    ADD CONSTRAINT client_id FOREIGN KEY ("клиент_id") REFERENCES public."клиент"(id);


--
-- TOC entry 5170 (class 2606 OID 19323)
-- Name: клиент client_user_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."клиент"
    ADD CONSTRAINT client_user_id_fk FOREIGN KEY ("пользователь_id") REFERENCES public."пользователь"(id) NOT VALID;


--
-- TOC entry 5209 (class 2606 OID 19328)
-- Name: тренер_и_клиент coach_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренер_и_клиент"
    ADD CONSTRAINT coach_id FOREIGN KEY ("тренер_id") REFERENCES public."тренер"(id);


--
-- TOC entry 5210 (class 2606 OID 19333)
-- Name: тренер_и_специальность coach_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренер_и_специальность"
    ADD CONSTRAINT coach_id FOREIGN KEY ("тренер_id") REFERENCES public."тренер"(id);


--
-- TOC entry 5211 (class 2606 OID 19338)
-- Name: тренер_и_специальность coach_speciality_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренер_и_специальность"
    ADD CONSTRAINT coach_speciality_id FOREIGN KEY ("специальность_тренера_id") REFERENCES public."специальность_тренера"(id);


--
-- TOC entry 5175 (class 2606 OID 19343)
-- Name: тренер coach_user_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренер"
    ADD CONSTRAINT coach_user_id_fk FOREIGN KEY ("пользователь_id") REFERENCES public."пользователь"(id) NOT VALID;


--
-- TOC entry 5194 (class 2606 OID 19348)
-- Name: дневник_и_чувство diary_and_feeling_diary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."дневник_и_чувство"
    ADD CONSTRAINT diary_and_feeling_diary_id_fkey FOREIGN KEY ("дневник_id") REFERENCES public."дневник"(id);


--
-- TOC entry 5195 (class 2606 OID 19353)
-- Name: дневник_и_чувство diary_and_feeling_feeling_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."дневник_и_чувство"
    ADD CONSTRAINT diary_and_feeling_feeling_id_fkey FOREIGN KEY ("чувство_id") REFERENCES public."чувство"(id);


--
-- TOC entry 5192 (class 2606 OID 19358)
-- Name: дневник_и_причина_чувства diary_and_reason_of_feeling_diary_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."дневник_и_причина_чувства"
    ADD CONSTRAINT diary_and_reason_of_feeling_diary_id_fkey FOREIGN KEY ("дневник_id") REFERENCES public."дневник"(id);


--
-- TOC entry 5193 (class 2606 OID 19363)
-- Name: дневник_и_причина_чувства diary_and_reason_of_feeling_reason_of_feeling_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."дневник_и_причина_чувства"
    ADD CONSTRAINT diary_and_reason_of_feeling_reason_of_feeling_id_fkey FOREIGN KEY ("причина_чувства_id") REFERENCES public."причина_чувства"(id);


--
-- TOC entry 5176 (class 2606 OID 19368)
-- Name: дневник diary_file_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."дневник"
    ADD CONSTRAINT diary_file_id_fkey FOREIGN KEY ("файл_id") REFERENCES public."файл"(id) NOT VALID;


--
-- TOC entry 5177 (class 2606 OID 19373)
-- Name: дневник diary_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."дневник"
    ADD CONSTRAINT diary_user_id_fkey FOREIGN KEY ("пользователь_id") REFERENCES public."пользователь"(id) NOT VALID;


--
-- TOC entry 5218 (class 2606 OID 19378)
-- Name: упражнение_и_снаряжение exercise_and_equipment_equipment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."упражнение_и_снаряжение"
    ADD CONSTRAINT exercise_and_equipment_equipment_id_fkey FOREIGN KEY ("снаряжение_id") REFERENCES public."снаряжение"(id) NOT VALID;


--
-- TOC entry 5220 (class 2606 OID 19383)
-- Name: упражнение_и_файл exercise_and_file_exercise_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."упражнение_и_файл"
    ADD CONSTRAINT exercise_and_file_exercise_id_fkey FOREIGN KEY ("упражнение_id") REFERENCES public."упражнение"(id);


--
-- TOC entry 5221 (class 2606 OID 19388)
-- Name: упражнение_и_файл exercise_and_file_file_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."упражнение_и_файл"
    ADD CONSTRAINT exercise_and_file_file_id_fkey FOREIGN KEY ("файл_id") REFERENCES public."файл"(id);


--
-- TOC entry 5178 (class 2606 OID 19393)
-- Name: упражнение_и_мыщца exercise_and_muscle_muscle_priority_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."упражнение_и_мыщца"
    ADD CONSTRAINT exercise_and_muscle_muscle_priority_id_fkey FOREIGN KEY ("приоритет_мышцы_id") REFERENCES public."приоритет_мышцы"(id) NOT VALID;


--
-- TOC entry 5181 (class 2606 OID 19398)
-- Name: упражнение exercise_exercise_difficulty_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."упражнение"
    ADD CONSTRAINT exercise_exercise_difficulty_id_fkey FOREIGN KEY ("сложность_упражнения_id") REFERENCES public."сложность_упражнения"(id) NOT VALID;


--
-- TOC entry 5182 (class 2606 OID 19403)
-- Name: упражнение exercise_exercise_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."упражнение"
    ADD CONSTRAINT exercise_exercise_type_id_fkey FOREIGN KEY ("тип_упражнения_id") REFERENCES public."тип_упражнения"(id) NOT VALID;


--
-- TOC entry 5188 (class 2606 OID 19408)
-- Name: тренировка_и_упражнение exercise_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренировка_и_упражнение"
    ADD CONSTRAINT exercise_id FOREIGN KEY ("упражнение_id") REFERENCES public."упражнение"(id) NOT VALID;


--
-- TOC entry 5216 (class 2606 OID 19413)
-- Name: упражнение_и_пользователь exercise_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."упражнение_и_пользователь"
    ADD CONSTRAINT exercise_id FOREIGN KEY ("упражнение_id") REFERENCES public."упражнение"(id);


--
-- TOC entry 5179 (class 2606 OID 19418)
-- Name: упражнение_и_мыщца exercise_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."упражнение_и_мыщца"
    ADD CONSTRAINT exercise_id FOREIGN KEY ("упражнение_id") REFERENCES public."упражнение"(id);


--
-- TOC entry 5219 (class 2606 OID 19423)
-- Name: упражнение_и_снаряжение exercise_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."упражнение_и_снаряжение"
    ADD CONSTRAINT exercise_id FOREIGN KEY ("упражнение_id") REFERENCES public."упражнение"(id) NOT VALID;


--
-- TOC entry 5200 (class 2606 OID 19428)
-- Name: отзыв feedback_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."отзыв"
    ADD CONSTRAINT feedback_client_id_fkey FOREIGN KEY ("клиент_id") REFERENCES public."клиент"(id);


--
-- TOC entry 5201 (class 2606 OID 19433)
-- Name: отзыв feedback_coach_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."отзыв"
    ADD CONSTRAINT feedback_coach_id_fkey FOREIGN KEY ("тренер_id") REFERENCES public."тренер"(id);


--
-- TOC entry 5222 (class 2606 OID 19438)
-- Name: файл_и_тип_файла file_and_file_type_file_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."файл_и_тип_файла"
    ADD CONSTRAINT file_and_file_type_file_id_fkey FOREIGN KEY ("файл_id") REFERENCES public."файл"(id);


--
-- TOC entry 5223 (class 2606 OID 19443)
-- Name: файл_и_тип_файла file_and_file_type_file_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."файл_и_тип_файла"
    ADD CONSTRAINT file_and_file_type_file_type_id_fkey FOREIGN KEY ("тип_файла_id") REFERENCES public."тип_файла"(id);


--
-- TOC entry 5206 (class 2606 OID 19448)
-- Name: сообщение_и_файл message_and_file_file_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."сообщение_и_файл"
    ADD CONSTRAINT message_and_file_file_id_fkey FOREIGN KEY ("файл_id") REFERENCES public."файл"(id);


--
-- TOC entry 5207 (class 2606 OID 19453)
-- Name: сообщение_и_файл message_and_file_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."сообщение_и_файл"
    ADD CONSTRAINT message_and_file_message_id_fkey FOREIGN KEY ("сообщение_id") REFERENCES public."сообщение"(id);


--
-- TOC entry 5180 (class 2606 OID 19458)
-- Name: упражнение_и_мыщца muscle_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."упражнение_и_мыщца"
    ADD CONSTRAINT muscle_id FOREIGN KEY ("мышца_id") REFERENCES public."мышца"(id);


--
-- TOC entry 5183 (class 2606 OID 19463)
-- Name: питание nutrition_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."питание"
    ADD CONSTRAINT nutrition_user_id_fkey FOREIGN KEY ("пользователь_id") REFERENCES public."пользователь"(id) NOT VALID;


--
-- TOC entry 5199 (class 2606 OID 19468)
-- Name: клиент_и_цель_тренировок purpose_of_workouts; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."клиент_и_цель_тренировок"
    ADD CONSTRAINT purpose_of_workouts FOREIGN KEY ("цель_тренировок_id") REFERENCES public."цель_тренировок"(id);


--
-- TOC entry 5184 (class 2606 OID 19473)
-- Name: шаги steps_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."шаги"
    ADD CONSTRAINT steps_user_id_fkey FOREIGN KEY ("пользователь_id") REFERENCES public."пользователь"(id) NOT VALID;


--
-- TOC entry 5174 (class 2606 OID 19478)
-- Name: клиент_и_подписка subscription_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."клиент_и_подписка"
    ADD CONSTRAINT subscription_id FOREIGN KEY ("подписка_id") REFERENCES public."подписка"(id);


--
-- TOC entry 5171 (class 2606 OID 19483)
-- Name: клиент training_level_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."клиент"
    ADD CONSTRAINT training_level_id FOREIGN KEY ("уровень_подготовки_id") REFERENCES public."уровень_подготовки"(id) NOT VALID;


--
-- TOC entry 5204 (class 2606 OID 19488)
-- Name: пользователь_и_достижение user_and_achievement_achievement_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."пользователь_и_достижение"
    ADD CONSTRAINT user_and_achievement_achievement_id_fkey FOREIGN KEY ("достижение_id") REFERENCES public."достижение"(id);


--
-- TOC entry 5205 (class 2606 OID 19493)
-- Name: пользователь_и_достижение user_and_achievement_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."пользователь_и_достижение"
    ADD CONSTRAINT user_and_achievement_user_id_fkey FOREIGN KEY ("пользователь_id") REFERENCES public."пользователь"(id);


--
-- TOC entry 5225 (class 2606 OID 19498)
-- Name: чат_и_пользователь user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."чат_и_пользователь"
    ADD CONSTRAINT user_id FOREIGN KEY ("пользователь_id") REFERENCES public."пользователь"(id);


--
-- TOC entry 5214 (class 2606 OID 19503)
-- Name: тренировка_и_пользователь user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренировка_и_пользователь"
    ADD CONSTRAINT user_id FOREIGN KEY ("пользователь_id") REFERENCES public."пользователь"(id);


--
-- TOC entry 5202 (class 2606 OID 19508)
-- Name: план_тренировки_и_пользователь user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."план_тренировки_и_пользователь"
    ADD CONSTRAINT user_id FOREIGN KEY ("пользователь_id") REFERENCES public."пользователь"(id);


--
-- TOC entry 5217 (class 2606 OID 19513)
-- Name: упражнение_и_пользователь user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."упражнение_и_пользователь"
    ADD CONSTRAINT user_id FOREIGN KEY ("пользователь_id") REFERENCES public."пользователь"(id);


--
-- TOC entry 5185 (class 2606 OID 19518)
-- Name: пользователь user_sex_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."пользователь"
    ADD CONSTRAINT user_sex_id_fk FOREIGN KEY ("пол_id") REFERENCES public."пол"(id) NOT VALID;


--
-- TOC entry 5186 (class 2606 OID 19523)
-- Name: вода water_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."вода"
    ADD CONSTRAINT water_user_id_fkey FOREIGN KEY ("пользователь_id") REFERENCES public."пользователь"(id) NOT VALID;


--
-- TOC entry 5187 (class 2606 OID 19528)
-- Name: вес weight_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."вес"
    ADD CONSTRAINT weight_user_id_fkey FOREIGN KEY ("пользователь_id") REFERENCES public."пользователь"(id) NOT VALID;


--
-- TOC entry 5189 (class 2606 OID 19533)
-- Name: тренировка_и_упражнение workout_and_exercise_exercise_stage_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренировка_и_упражнение"
    ADD CONSTRAINT workout_and_exercise_exercise_stage_id_fkey FOREIGN KEY ("этап_упражнения_id") REFERENCES public."этап_упражнения"(id) NOT VALID;


--
-- TOC entry 5215 (class 2606 OID 19538)
-- Name: тренировка_и_пользователь workout_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренировка_и_пользователь"
    ADD CONSTRAINT workout_id FOREIGN KEY ("тренировка_id") REFERENCES public."тренировка"(id);


--
-- TOC entry 5212 (class 2606 OID 19543)
-- Name: тренировка_и_план_тренировки workout_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренировка_и_план_тренировки"
    ADD CONSTRAINT workout_id FOREIGN KEY ("тренировка_id") REFERENCES public."тренировка"(id);


--
-- TOC entry 5190 (class 2606 OID 19548)
-- Name: тренировка_и_упражнение workout_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренировка_и_упражнение"
    ADD CONSTRAINT workout_id FOREIGN KEY ("тренировка_id") REFERENCES public."тренировка"(id) NOT VALID;


--
-- TOC entry 5213 (class 2606 OID 19553)
-- Name: тренировка_и_план_тренировки workout_plan_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."тренировка_и_план_тренировки"
    ADD CONSTRAINT workout_plan_id FOREIGN KEY ("план_тренировки_id") REFERENCES public."план_тренировки"(id);


--
-- TOC entry 5203 (class 2606 OID 19558)
-- Name: план_тренировки_и_пользователь workout_plan_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."план_тренировки_и_пользователь"
    ADD CONSTRAINT workout_plan_id FOREIGN KEY ("план_тренировки_id") REFERENCES public."план_тренировки"(id) NOT VALID;


--
-- TOC entry 5197 (class 2606 OID 19563)
-- Name: клиент_и_тип_тренировки workout_type_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."клиент_и_тип_тренировки"
    ADD CONSTRAINT workout_type_id FOREIGN KEY ("тип_тренировки_id") REFERENCES public."тип_тренировки"(id);


-- Completed on 2025-04-16 21:54:22

--
-- PostgreSQL database dump complete
--

