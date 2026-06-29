import React, { useState, useEffect } from 'react';
import ProyectosCliente from './ProyectosCliente';
import axios from 'axios';
import './App.css';

function App() {
  const API_CLIENTES = "http://127.0.0.1:8000/clientes/";
  const API_IA = "http://127.0.0.1:8000/ia/generar-correo";
  const API_PROYECTOS = "http://127.0.0.1:8000/proyectos/";
  const API_CORREO = "http://127.0.0.1:8000/correo/enviar";

  // --- ESTADOS DE AUTENTICACIÓN ---
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("token"));
  const [mostrarRegistro, setMostrarRegistro] = useState(false);
  const [authEmail, setAuthEmail] = useState('');
  const [authPassword, setAuthPassword] = useState('');
  const [authNombre, setAuthNombre] = useState('');

  // --- ESTADOS DE CLIENTES Y PANEL ---
  const [clientes, setClientes] = useState([]);
  const [nuevoCliente, setNuevoCliente] = useState({
    nombre: "",
    empresa: "",
    email: "",
    telefono: "",
    password: ""
  });
  const [clienteSeleccionado, setClienteSeleccionado] = useState(null);
  const [proyectosCliente, setProyectosCliente] = useState([]);
  const [nombreProyecto, setNombreProyecto] = useState('');
  const [descProyecto, setDescProyecto] = useState('');

  // --- ESTADOS DE LA IA (Para el mensaje) ---
  const [detalleProyecto, setDetalleProyecto] = useState('');
  const [tono, setTono] = useState('profesional');
  const [correoGenerated, setCorreoGenerated] = useState(null);
  const [cargandoIA, setCargandoIA] = useState(false);
  const usuario = JSON.parse(
    localStorage.getItem("usuario")
  );



  // Cargar clientes automáticamente si ya está logueado
  const obtenerClientes = async () => {
    try {
      const tokenDinamico = localStorage.getItem("token");
      const res = await axios.get(API_CLIENTES, {
        headers: { Authorization: `Bearer ${tokenDinamico}` }
      });
      setClientes(res.data);
    } catch (error) {
      console.error("Error al obtener clientes:", error);
    }
  };

  const crearCliente = async (e) => {

    e.preventDefault();

    try {

      const token = localStorage.getItem("token");

      await axios.post(
        API_CLIENTES,
        nuevoCliente,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      alert("Cliente creado correctamente.");

      setNuevoCliente({
        nombre: "",
        empresa: "",
        email: "",
        telefono: "",
        password: ""
      });

      obtenerClientes();

    } catch (error) {

      console.log(error);

      alert(
        error.response?.data?.detail ||
        "Error al crear cliente."
      );

    }

  }

  useEffect(() => {
    if (isLoggedIn) {
      obtenerClientes();
    }
  }, [isLoggedIn]);

  const manejarLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://127.0.0.1:8000/auth/login", {
        email: authEmail,
        password: authPassword // Viaja el texto plano que escribes
      });

      localStorage.setItem("token", res.data.access_token);
      localStorage.setItem(
        "usuario",
        JSON.stringify(res.data.usuario)
      );
      setIsLoggedIn(true);
      alert("¡Bienvenido de nuevo!");

      // Limpieza absoluta de inputs
      setAuthEmail('');
      setAuthPassword('');
    } catch (error) {
      console.error(error);
      alert("Credenciales incorrectas o error en el servidor");
    }
  };

  const manejarRegistro = async (e) => {
    e.preventDefault();
    try {
      // Mandamos el objeto con los datos reales de tus estados
      await axios.post("http://127.0.0.1:8000/auth/registro", {
        nombre: authNombre,
        email: authEmail,
        password: authPassword,
        tipo_usuario: "Freelancer"
      });

      alert("¡Registro exitoso! Ya puedes iniciar sesión.");
      setMostrarRegistro(false);

      // Limpieza absoluta para que no se herede la clave en el login
      setAuthNombre('');
      setAuthEmail('');
      setAuthPassword('');
    } catch (error) {
      console.error(error);
      alert("Error en el registro. Verifica los campos.");
    }
  };

  const cerrarSesion = () => {
    localStorage.removeItem("token");
    setIsLoggedIn(false);
    setClientes([]);
    setClienteSeleccionado(null);
  };

  // --- SELECCIONAR CLIENTE Y CARGAR SUS PROYECTOS ---
  const seleccionarCliente = async (cliente) => {
    setClienteSeleccionado(cliente);
    // Limpiar el correo anterior
    setCorreoGenerated("");

    // Limpiar el formulario
    setDetalleProyecto("");
    setTono("profesional");
    try {
      const tokenDinamico = localStorage.getItem("token");
      const res = await axios.get(`${API_PROYECTOS}cliente/${cliente.id}`, {
        headers: { Authorization: `Bearer ${tokenDinamico}` }
      });
      setProyectosCliente(res.data);
    } catch (error) {
      console.error("Error al cargar proyectos:", error);
    }
  };

  // --- ACCIÓN: ENVIAR MENSAJE / GENERAR CORREO IA ---
  const generarCorreoIA = async (e) => {

    e.preventDefault();

    if (!clienteSeleccionado) {
      alert("Seleccione un cliente.");
      return;
    }

    try {

      setCargandoIA(true);

      const token = localStorage.getItem("token");

      const res = await axios.post(

        API_IA,

        {
          cliente_id: clienteSeleccionado.id,
          detalles: detalleProyecto,
          tono: tono
        },

        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }

      );

      setCorreoGenerated(res.data);

      setDetalleProyecto("");
      setTono("profesional");

    }

    catch (error) {

      console.log(error.response);

      alert(
        error.response?.data?.detail ||
        "No se pudo generar el correo."
      );

    }

    finally {

      setCargandoIA(false);

    }

  }

  const enviarCorreo = async () => {

    if (!correoGenerated) {
      alert("Primero genera un correo.");
      return;
    }

    try {

      const token = localStorage.getItem("token");

      await axios.post(
        API_CORREO,
        {
          cliente_id: clienteSeleccionado.id,
          asunto: correoGenerated.asunto,
          contenido: correoGenerated.correo
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      alert("Correo enviado correctamente.");

    } catch (error) {

      console.log(error);

      alert(
        error.response?.data?.detail ||
        "No fue posible enviar el correo."
      );
    }

  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      {!isLoggedIn ? (
        /* ================= VISTA 1: ANTES DE ENTRAR (LOGIN / REGISTRO) ================= */
        <div className="max-w-md mx-auto mt-20 bg-gray-800 p-8 rounded-lg shadow-lg border border-gray-700">
          {mostrarRegistro ? (
            <form onSubmit={manejarRegistro} className="space-y-4">
              <h2 className="text-2xl font-bold text-center text-blue-400">Crear Cuenta</h2>
              <input
                type="text" placeholder="Nombre completo" required className="w-full p-2.5 rounded bg-gray-700 text-white border border-gray-600 focus:outline-none"
                value={authNombre} onChange={(e) => setAuthNombre(e.target.value)}
                autoComplete="off"
              />
              <input
                type="email" placeholder="Correo electrónico" required className="w-full p-2.5 rounded bg-gray-700 text-white border border-gray-600 focus:outline-none"
                value={authEmail} onChange={(e) => setAuthEmail(e.target.value)}
                autoComplete="off"
              />
              <input
                type="password"
                placeholder="Contraseña"
                required
                className="w-full p-2.5 rounded bg-gray-700 text-white border border-gray-600 focus:outline-none"
                value={authPassword}
                onChange={(e) => setAuthPassword(e.target.value)}
                autoComplete="new-password"
              />
              <button type="submit" className="w-full bg-green-600 hover:bg-green-700 p-2.5 rounded font-bold">Registrarse</button>
              <p className="text-sm text-center text-gray-400 mt-2">
                ¿Ya tienes cuenta? <button type="button" onClick={() => setMostrarRegistro(false)} className="text-blue-400 underline bg-none border-none p-0 cursor-pointer">Inicia Sesión</button>
              </p>
            </form>
          ) : (
            <form onSubmit={manejarLogin} className="space-y-4">
              <h2 className="text-2xl font-bold text-center text-blue-400">Iniciar Sesión</h2>
              <input
                type="email" placeholder="Correo electrónico" required className="w-full p-2.5 rounded bg-gray-700 text-white border border-gray-600 focus:outline-none"
                value={authEmail} onChange={(e) => setAuthEmail(e.target.value)}
              />
              <input
                type="password" placeholder="Contraseña" required className="w-full p-2.5 rounded bg-gray-700 text-white border border-gray-600 focus:outline-none"
                value={authPassword} onChange={(e) => setAuthPassword(e.target.value)}
              />
              <button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 p-2.5 rounded font-bold">Ingresar</button>
              <p className="text-sm text-center text-gray-400 mt-2">
                ¿No tienes cuenta? <button type="button" onClick={() => setMostrarRegistro(true)} className="text-green-400 underline bg-none border-none p-0 cursor-pointer">Regístrate aquí</button>
              </p>
            </form>
          )}
        </div>
      ) : (
        /* ================= VISTA 2: DENTRO DE LA APP (CRM COMPLETO) ================= */
        <div className="space-y-6">
          <header className="flex justify-between items-center border-b border-gray-700 pb-4">

            <div>

              <h1 className="text-3xl font-bold text-blue-400">
                Panel CRM Freelancers
              </h1>

              <p className="text-gray-300 mt-2">
                Bienvenido,
                <span className="text-green-400 font-bold">
                  {" "}{usuario?.nombre}
                </span>
              </p>

              <p className="text-sm text-gray-500">
                Rol:
                <span className="text-yellow-400 font-semibold">
                  {" "}{usuario?.rol}
                </span>
              </p>

            </div>

            <button
              onClick={cerrarSesion}
              className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded font-bold text-sm"
            >
              Cerrar Sesión
            </button>

          </header>

          <main className="grid grid-cols-1 lg:grid-cols-3 gap-6">

            {/* COLUMNA 1: LISTA DE CLIENTES */}
            <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700 space-y-4">
              <form
                onSubmit={crearCliente}
                className="space-y-2 mb-6"
              >

                <h3 className="text-lg font-bold text-blue-400">
                  Nuevo Cliente
                </h3>

                <input
                  type="text"
                  placeholder="Nombre"
                  className="w-full p-2 rounded bg-gray-700"
                  value={nuevoCliente.nombre}
                  onChange={(e) => setNuevoCliente({ ...nuevoCliente, nombre: e.target.value })}
                  required
                />

                <input
                  type="text"
                  placeholder="Empresa"
                  className="w-full p-2 rounded bg-gray-700"
                  value={nuevoCliente.empresa}
                  onChange={(e) => setNuevoCliente({ ...nuevoCliente, empresa: e.target.value })}
                />

                <input
                  type="email"
                  placeholder="Correo"
                  className="w-full p-2 rounded bg-gray-700"
                  value={nuevoCliente.email}
                  onChange={(e) => setNuevoCliente({ ...nuevoCliente, email: e.target.value })}
                  required
                />

                <input
                  type="text"
                  placeholder="Teléfono"
                  className="w-full p-2 rounded bg-gray-700"
                  value={nuevoCliente.telefono}
                  onChange={(e) => setNuevoCliente({ ...nuevoCliente, telefono: e.target.value })}
                />

                <input
                  type="password"
                  placeholder="Contraseña"
                  className="w-full p-2 rounded bg-gray-700"
                  value={nuevoCliente.password}
                  onChange={(e) => setNuevoCliente({ ...nuevoCliente, password: e.target.value })}
                  required
                />

                <button
                  className="w-full bg-green-600 hover:bg-green-700 p-2 rounded font-bold"
                >
                  Crear Cliente
                </button>

              </form>
              <h3 className="text-xl font-bold text-gray-300">Clientes Disponibles</h3>

              <div className="space-y-2">
                {clientes.map((c) => (
                  <div
                    key={c.id} onClick={() => seleccionarCliente(c)}
                    className={`p-3 rounded border cursor-pointer transition-all ${clienteSeleccionado?.id === c.id ? 'bg-blue-900/40 border-blue-500' : 'bg-gray-700/50 border-gray-600 hover:bg-gray-700'}`}
                  >
                    <p className="font-bold">{c.nombre}</p>
                    <p className="text-xs text-gray-400">{c.email}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* COLUMNA 2: FORMULARIO DE ENVÍO DE MENSAJE (IA) */}
            <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700 space-y-4">
              <h3 className="text-xl font-bold text-gray-300">Enviar Mensaje con IA</h3>
              {clienteSeleccionado ? (
                <form onSubmit={generarCorreoIA} className="space-y-4">
                  <p className="text-sm text-gray-400">Enviando a: <span className="text-blue-400 font-bold">{clienteSeleccionado.nombre}</span></p>

                  <div>
                    <label className="block text-xs text-gray-400 mb-1">Detalle o Motivo del Mensaje</label>
                    <textarea
                      rows="4" required placeholder="Ej: Informar que el diseño del home está listo para revisión..."
                      className="w-full p-2 rounded bg-gray-700 border border-gray-600 text-sm focus:outline-none"
                      value={detalleProyecto} onChange={(e) => setDetalleProyecto(e.target.value)}
                    />
                  </div>

                  <div>
                    <label className="block text-xs text-gray-400 mb-1">Tono del Mensaje</label>
                    <select
                      className="w-full p-2 rounded bg-gray-700 border border-gray-600 text-sm"
                      value={tono} onChange={(e) => setTono(e.target.value)}
                    >
                      <option value="profesional">Profesional</option>
                      <option value="formal">Formal</option>
                      <option value="amigable">Amigable</option>
                    </select>
                  </div>

                  <button type="submit" disabled={cargandoIA} className="w-full bg-blue-600 hover:bg-blue-700 p-2.5 rounded font-bold text-sm">
                    {cargandoIA ? "Generando..." : "Generar Correo con IA"}
                  </button>
                </form>
              ) : (
                <p className="text-sm text-gray-500">Selecciona un cliente a la izquierda para redactar un mensaje.</p>
              )}
            </div>

            {/* COLUMNA 3: PROYECTOS DEL CLIENTE ACTIVO Y RESULTADO */}
            <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700 space-y-4">
              <h3 className="text-xl font-bold text-gray-300">Historial y Proyectos</h3>

              {/* Si la IA generó un correo, lo mostramos aquí */}
              {clienteSeleccionado && correoGenerated && (

                <>
                  <div className="bg-gray-800 border border-green-500 rounded-lg p-5 shadow-lg">

                    <h3 className="text-xl font-bold text-green-400 mb-4">
                      Correo generado por IA
                    </h3>

                    <div className="space-y-2 text-sm">

                      <div>
                        <span className="font-bold text-gray-300">De:</span>
                        <p className="text-white">{correoGenerated.remitente}</p>
                        <p className="text-gray-400">{correoGenerated.correo_remitente}</p>
                      </div>

                      <hr className="border-gray-600" />

                      <div>
                        <span className="font-bold text-gray-300">Para:</span>
                        <p className="text-white">{correoGenerated.destinatario}</p>
                        <p className="text-gray-400">{correoGenerated.correo_destinatario}</p>
                      </div>

                      <hr className="border-gray-600" />

                      <div>
                        <span className="font-bold text-gray-300">
                          Empresa
                        </span>

                        <p className="text-white">
                          {correoGenerated.empresa}
                        </p>
                      </div>

                      <hr className="border-gray-600" />

                      <div>
                        <span className="font-bold text-gray-300">
                          Asunto
                        </span>

                        <p className="text-white">
                          {correoGenerated.asunto}
                        </p>
                      </div>

                    </div>

                    <div className="mt-5 border-t border-gray-600 pt-4">

                      <pre className="whitespace-pre-wrap text-sm text-gray-200 font-sans">
                        {correoGenerated.correo}
                      </pre>

                    </div>

                    <button
                      onClick={enviarCorreo}
                      className="mt-5 w-full bg-green-600 hover:bg-green-700 p-3 rounded font-bold transition"
                    >
                      📧 Enviar Correo
                    </button>

                  </div>

                </>

              )}

              {clienteSeleccionado && (
                <div className="pt-2">
                  <p className="text-sm font-semibold text-gray-400 mb-2">Proyectos de este cliente:</p>
                  <ProyectosCliente proyectos={proyectosCliente} clienteId={clienteSeleccionado.id} />
                </div>
              )}
            </div>

          </main>
        </div>
      )}
    </div>
  );
}

export default App;