package com.misitioweb.miappnotas.data.repository

import com.misitioweb.miappnotas.data.local.Nota
import com.misitioweb.miappnotas.data.local.NotaDao
import kotlinx.coroutines.flow.Flow

class NotaRepositorio(private val notaDao: NotaDao) {
    
    val todasLasNotas: Flow<List<Nota>> = notaDao.obtenerTodas()
    
    suspend fun obtenerPorId(id: Long): Nota? = notaDao.obtenerPorId(id)
    
    suspend fun insertar(nota: Nota): Long = notaDao.insertar(nota)
    
    suspend fun actualizar(nota: Nota) = notaDao.actualizar(nota)
    
    suspend fun eliminar(nota: Nota) = notaDao.eliminar(nota)
}