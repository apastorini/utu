package com.misitioweb.miappnotas.data.local

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import kotlinx.coroutines.flow.Flow

@Dao
interface NotaDao {
    
    @Query("SELECT * FROM notas ORDER BY fechaCreacion DESC")
    fun obtenerTodas(): Flow<List<Nota>>
    
    @Query("SELECT * FROM notas WHERE id = :id")
    suspend fun obtenerPorId(id: Long): Nota?
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertar(nota: Nota): Long
    
    @Update
    suspend fun actualizar(nota: Nota)
    
    @Delete
    suspend fun eliminar(nota: Nota)
}