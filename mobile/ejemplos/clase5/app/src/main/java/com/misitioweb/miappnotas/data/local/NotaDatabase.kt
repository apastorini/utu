package com.misitioweb.miappnotas.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(entities = [Nota::class], version = 1, exportSchema = false)
abstract class NotaDatabase : RoomDatabase() {
    
    abstract fun notaDao(): NotaDao
    
    companion object {
        @Volatile
        private var INSTANCIA: NotaDatabase? = null
        
        fun obtener(context: Context): NotaDatabase {
            return INSTANCIA ?: synchronized(this) {
                val base = Room.databaseBuilder(
                    context.applicationContext,
                    NotaDatabase::class.java,
                    "notas_db"
                ).build()
                INSTANCIA = base
                base
            }
        }
    }
}