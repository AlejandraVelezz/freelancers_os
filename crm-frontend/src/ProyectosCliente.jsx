import React from 'react';

const ProyectosCliente = ({ proyectos }) => {
  if (!proyectos || proyectos.length === 0) {
    return (
      <div className="text-center py-6 bg-white rounded-xl border border-dashed border-gray-200 p-4 mt-4">
        <p className="text-gray-400 text-sm">Este cliente no tiene proyectos asignados.</p>
      </div>
    );
  }

  return (
    <div className="bg-gray-50 p-6 rounded-2xl border border-gray-100 mt-6">
      <div className="flex justify-between items-center mb-4">
        <div>
          <h3 className="text-base font-bold text-gray-800">Proyectos del Cliente</h3>
          <p className="text-xs text-gray-400">Presupuestos y estados en tiempo real</p>
        </div>
        <span className="bg-indigo-50 text-indigo-700 text-xs font-semibold px-2.5 py-1 rounded-full">
          {proyectos.length} Activos
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {proyectos.map((proy) => (
          <div key={proy.id} className="bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-all p-5 flex flex-col justify-between">
            <div>
              <div className="flex justify-between items-start mb-2">
                <h4 className="font-bold text-gray-800 text-sm">{proy.nombre}</h4>
                <span className={`px-2 py-0.5 rounded-full text-[10px] font-medium border ${
                  proy.estado === 'Completado' ? 'bg-green-50 text-green-700 border-green-200' :
                  proy.estado === 'En Progreso' ? 'bg-blue-50 text-blue-700 border-blue-200' :
                  'bg-amber-50 text-amber-700 border-amber-200'
                }`}>
                  {proy.estado || 'Pendiente'}
                </span>
              </div>
              <p className="text-gray-500 text-xs line-clamp-2 mb-3">{proy.descripcion}</p>
              <div className="text-[11px] text-gray-400 pt-2 border-t border-gray-50 space-y-1">
                <div>📅 Entrega: <strong className="text-gray-600">{proy.fecha_entrega || 'Por definir'}</strong></div>
                <div>💰 Presupuesto: <strong className="text-gray-700">${Number(proy.presupuesto).toLocaleString()}</strong></div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProyectosCliente;