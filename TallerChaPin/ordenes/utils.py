def requiere_insumo(tareas): 
  materiales = False
  repuestos = False
  requerimientos = {"materiales": materiales, "repuestos": repuestos}

  for t in tareas:
      materiales |= t.tipo.materiales
      repuestos |= t.tipo.repuestos

  requerimientos = {"materiales": materiales, "repuestos": repuestos}
  return requerimientos