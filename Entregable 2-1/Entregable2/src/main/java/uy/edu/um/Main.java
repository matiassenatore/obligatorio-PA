package uy.edu.um;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class Main {
    public static void main(String[] args) {
        ProcesadorDePedidos procesador = new ProcesadorDePedidos(10);

        // Executor para simular generación secuencial de pedidos
        ExecutorService generadorDePedidos = Executors.newSingleThreadExecutor();

        // Simulación de generación secuencial de pedidos
        generadorDePedidos.submit(() -> {
            for (int i = 1; i <= 100; i++) {
                try {
                    // Genera un ID secuencial
                    int id = i;
                    // El pedido es urgente si el ID es par, de lo contrario, es normal
                    Pedido pedido = new Pedido(id, (id % 2 == 0) ? 1 : 2);

                    // Agrega el pedido a la cola de procesamiento
                    procesador.agregarPedido(pedido);

                    // Pausa para simular que los pedidos no se generan todos al mismo tiempo
                    Thread.sleep((long) (Math.random() * 300));  // Pausa entre 0 y 300 ms
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });

        // Procesamiento de los pedidos en paralelo
        procesador.procesarPedidos();

        // Cierre del generador de pedidos y pool de hilos
        generadorDePedidos.shutdown();
        try {
            generadorDePedidos.awaitTermination(1, TimeUnit.MINUTES);  // Espera a que terminen de generarse todos los pedidos
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        procesador.shutdown();  // Cierra el pool de hilos una vez que todos los pedidos han sido procesados
    }
}
