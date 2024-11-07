package uy.edu.um;

import java.util.concurrent.*;

public class ProcesadorDePedidos {
    private final ForkJoinPool forkJoinPool;
    private final ProcesadorDePago procesadorDePago = new ProcesadorDePago();
    private final ProcesadorDeEmpaquetado procesadorDeEmpaquetado = new ProcesadorDeEmpaquetado();
    private final ProcesadorDeEnvio procesadorDeEnvio = new ProcesadorDeEnvio();

    // Cola de prioridad para los pedidos
    private final PriorityBlockingQueue<Pedido> colaPedidos = new PriorityBlockingQueue<>();

    public ProcesadorDePedidos(int numThreads) {
        this.forkJoinPool = new ForkJoinPool(numThreads);
        System.out.println("Iniciando Procesador de Pedidos con " + numThreads + " hilos.");
    }

    // Método para agregar un pedido a la cola
    public void agregarPedido(Pedido pedido) {
        System.out.println("Pedido generado: " + pedido);
        colaPedidos.put(pedido);  // Añade el pedido a la cola de prioridad
    }

    // Método para procesar los pedidos en la cola
    public void procesarPedidos() {
        System.out.println("Iniciando el procesamiento de pedidos...");
        forkJoinPool.execute(() -> {
            while (true) {
                try {
                    Pedido pedido = colaPedidos.take();  // Toma el pedido de mayor prioridad
                    procesarPedido(pedido);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
                if (forkJoinPool.isShutdown() && colaPedidos.isEmpty()) {
                    break;
                }
            }
        });
    }

    private void procesarPedido(Pedido pedido) {
        System.out.println("Procesando pedido: " + pedido);
        procesadorDePago.procesarPago(pedido);
        procesadorDeEmpaquetado.empacarPedido(pedido);
        procesadorDeEnvio.enviarPedido(pedido);
    }

    public void shutdown() {
        System.out.println("Iniciando el cierre de hilos...");
        forkJoinPool.shutdown();
        try {
            if (!forkJoinPool.awaitTermination(60, TimeUnit.SECONDS)) {
                forkJoinPool.shutdownNow();
                System.out.println("Cierre forzado de hilos.");
            } else {
                System.out.println("Hilos cerrados correctamente.");
            }
        } catch (InterruptedException e) {
            forkJoinPool.shutdownNow();
            System.out.println("Cierre forzado de hilos debido a interrupción.");
        }
    }

    public boolean isShutdown() {
        return forkJoinPool.isShutdown();
    }

    public void esperarTerminacion() throws InterruptedException {
        forkJoinPool.awaitTermination(1, TimeUnit.MINUTES);
    }

}


