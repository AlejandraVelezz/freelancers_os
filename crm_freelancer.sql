-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 20-06-2026 a las 03:11:57
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `crm_freelancer`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `empresa` varchar(150) DEFAULT NULL,
  `email` varchar(150) NOT NULL,
  `telefono` varchar(50) DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id`, `nombre`, `empresa`, `email`, `telefono`, `usuario_id`) VALUES
(1, 'string', 'string', 'user@example.com', 'string', NULL),
(2, 'Juan', 'Salud', 'juan@gmail.com', '3245678945', NULL),
(3, 'Alexander', 'Cocoa', 'alexander@gmail.com', '32166933399', NULL),
(4, 'Maria', 'Carnes SA', 'maria78@gmail.com', '123455', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `correos_historial`
--

CREATE TABLE `correos_historial` (
  `id` int(11) NOT NULL,
  `cliente_id` int(11) DEFAULT NULL,
  `proyecto` varchar(200) DEFAULT NULL,
  `contenido` text NOT NULL,
  `fecha` datetime DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `correos_historial`
--

INSERT INTO `correos_historial` (`id`, `cliente_id`, `proyecto`, `contenido`, `fecha`, `usuario_id`) VALUES
(1, 2, 'Tienda Virtual', 'Asunto: Actualización sobre Proyecto: Tienda Virtual\n\nEstimado Juan,\n\nMe dirijo a usted para informarle que el próximo paso en el proyecto de Tienda Virtual es el inicio del desarrollo del módulo de la aplicación. Esto se encuentra dentro del plan de trabajo establecido y se espera una entrega en la fecha prevista.\n\nSi tiene alguna pregunta o inquietud, por favor no dude en hacérmelo saber a través de este correo electrónico.\n\nAtentamente,\n[Tu nombre]', '2026-06-10 12:08:37', NULL),
(2, 2, 'Tienda Virtual', 'Asunto: Actualización sobre el Proyecto: Tienda Virtual\n\nEstimado Juan,\n\nMe dirijo a usted para informarle sobre un problema técnico detectado en el módulo de clientes de nuestra tienda virtual. Desafortunadamente, no hemos podido iniciar el servidor debido a un fallo en el registro del módulo.\n\nEstamos trabajando en solucionar el problema con urgencia para minimizar el impacto en el proyecto. Le mantendré informado sobre el progreso y le proporcionaré una estimación de tiempo para la resolución del mismo.\n\nSi necesita información adicional o desea discutir el asunto, por favor no dudar en hacérmelo saber.\n\nAtentamente,\n[Tu Nombre]', '2026-06-10 12:09:20', NULL),
(3, 3, 'web-empresarial', 'Asunto: Revisión del Proyecto Web-Empresarial - Corrección de Nombres de Módulos Iniciales\n\nEstimado Alexander,\n\nMe dirijo a usted con el fin de atender una queja formal referente al proyecto web-empresarial que estamos desarrollando. Después de revisar la solicitud, he identificado que el nombre de los módulos iniciales no se ajusta a los requisitos establecidos en el contrato.\n\nMe gustaría programar una reunión con usted para discutir la corrección de este detalle y asegurarnos de que se ajuste a sus expectativas. De esta manera, podremos avanzar con la implementación del proyecto sin que esto afecte la calidad final.\n\nAgradezco su atención a este asunto y espero su respuesta para programar la reunión.\n\nAtentamente,\n[Tu Nombre]', '2026-06-10 13:32:11', NULL),
(4, 4, 'Asignacion Modulo de Front', 'Asunto: Actualización del Proyecto: Asignación Modulo de Front\n\nEstimada María,\n\nMe dirijo a usted para informar que el proyecto \"Asignación Modulo de Front\" se encuentra en curso y hemos avanzado en la implementación de la función de \"Acceso inicial controlado para la app\".\n\nHemos logrado configurar un sistema de seguridad robusto que garantiza el acceso seguro a la aplicación. Nuestro equipo de trabajo ha trabajado incansablemente para cumplir con los plazos establecidos y asegurar la calidad del trabajo.\n\nSi necesita cualquier información adicional o desea programar una reunión para discutir los detalles del proyecto, por favor, no dude en hacérmelo saber.\n\nAtentamente,\n[Tu nombre]\nFreelancer', '2026-06-10 17:51:53', NULL),
(5, 4, 'Asignacion Modulo de Front', 'Asunto: Actualización del Proyecto: Asignación Modulo de Front\n\nEstimada María,\n\nMe dirijo a usted para informar que el proyecto \"Asignación Modulo de Front\" se encuentra en curso y hemos avanzado en la implementación de la función de \"Acceso inicial controlado para la app\".\n\nHemos logrado configurar un sistema de seguridad robusto que garantiza el acceso seguro a la aplicación. Nuestro equipo de trabajo ha trabajado incansablemente para cumplir con los plazos establecidos y asegurar la calidad del trabajo.\n\nSi necesita cualquier información adicional o desea programar una reunión para discutir los detalles del proyecto, por favor, no dude en hacérmelo saber.\n\nAtentamente,\n[Tu nombre]\nFreelancer', '2026-06-10 17:52:01', NULL),
(6, 2, 'Tienda Virtual', 'Asunto: Progreso del Proyecto: Tienda Virtual\n\nEstimado Juan,\n\nMe dirijo a usted para informarle que hemos alcanzado el día 2 de la continuación del módulo correspondiente al proyecto \"Tienda Virtual\". En esta etapa, hemos completado la revisión inicial y estamos listos para avanzar con los siguientes pasos.\n\nSi necesitas información adicional o tienes alguna pregunta, por favor no dudes en hacérmelo saber.\n\nAtentamente,\n[Tu nombre]', '2026-06-10 19:52:55', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notificaciones`
--

CREATE TABLE `notificaciones` (
  `id` int(11) NOT NULL,
  `cliente_id` int(11) DEFAULT NULL,
  `asunto` varchar(200) NOT NULL,
  `mensaje` text NOT NULL,
  `estado` varchar(50) DEFAULT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proyectos`
--

CREATE TABLE `proyectos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` varchar(50) DEFAULT NULL,
  `cliente_id` int(11) DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proyectos`
--

INSERT INTO `proyectos` (`id`, `nombre`, `descripcion`, `estado`, `cliente_id`, `usuario_id`) VALUES
(1, 'Tienda Virtual', 'Inicio del back', 'Nuevo', 2, NULL),
(2, 'Software de Gestion ', '', 'Nuevo', 1, NULL),
(3, 'web-empresarial', '', 'Nuevo', 3, NULL),
(4, 'Asignacion Modulo de Front', '', 'Nuevo', 4, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tareas`
--

CREATE TABLE `tareas` (
  `id` int(11) NOT NULL,
  `titulo` varchar(150) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` varchar(50) DEFAULT NULL,
  `proyecto_id` int(11) DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tareas`
--

INSERT INTO `tareas` (`id`, `titulo`, `descripcion`, `estado`, `proyecto_id`, `usuario_id`) VALUES
(1, 'Iniciar Algoritmo', NULL, 'Pendiente', 2, NULL),
(2, 'Definicion de variables iniciales', NULL, 'Pendiente', 2, NULL),
(3, 'FrontEnd app', NULL, 'Pendiente', 4, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `tipo_usuario` varchar(100) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_clientes_email` (`email`),
  ADD KEY `ix_clientes_id` (`id`),
  ADD KEY `fk_clientes_usuarios` (`usuario_id`);

--
-- Indices de la tabla `correos_historial`
--
ALTER TABLE `correos_historial`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cliente_id` (`cliente_id`),
  ADD KEY `ix_correos_historial_id` (`id`),
  ADD KEY `fk_correos_usuarios` (`usuario_id`);

--
-- Indices de la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cliente_id` (`cliente_id`),
  ADD KEY `ix_notificaciones_id` (`id`),
  ADD KEY `fk_notificaciones_usuarios` (`usuario_id`);

--
-- Indices de la tabla `proyectos`
--
ALTER TABLE `proyectos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cliente_id` (`cliente_id`),
  ADD KEY `ix_proyectos_id` (`id`),
  ADD KEY `fk_proyectos_usuarios` (`usuario_id`);

--
-- Indices de la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_tareas_id` (`id`),
  ADD KEY `fk_tareas_proyectos` (`proyecto_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `correos_historial`
--
ALTER TABLE `correos_historial`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `proyectos`
--
ALTER TABLE `proyectos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `tareas`
--
ALTER TABLE `tareas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD CONSTRAINT `fk_clientes_usuarios` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `correos_historial`
--
ALTER TABLE `correos_historial`
  ADD CONSTRAINT `correos_historial_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_correos_usuarios` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  ADD CONSTRAINT `fk_notificaciones_usuarios` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `notificaciones_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `proyectos`
--
ALTER TABLE `proyectos`
  ADD CONSTRAINT `fk_proyectos_usuarios` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `proyectos_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD CONSTRAINT `fk_tareas_proyectos` FOREIGN KEY (`proyecto_id`) REFERENCES `proyectos` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `tareas_ibfk_1` FOREIGN KEY (`proyecto_id`) REFERENCES `proyectos` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
