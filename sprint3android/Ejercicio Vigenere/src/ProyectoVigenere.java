import java.io.*;
import java.net.*;
import java.time.LocalDate;
import java.util.Scanner;

public class ProyectoVigenere {

    static String[] calles = {"CLAVELES", "HORTENSIAS", "LIRIOS", "MARGARITAS", "ORQUIDEAS", "PETUNIAS", "TULIPANES"};
    static String[] diasSemana = {"LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO", "DOMINGO"};
    static String alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    public static void main(String[] args) {
        Thread threadServidor = new Thread(() -> servidor());
        threadServidor.setDaemon(true);
        threadServidor.start();

        try { Thread.sleep(500); } catch (InterruptedException e) {}

        cliente();
    }

    public static void servidor() {
        try (ServerSocket serverSocket = new ServerSocket(5000)) {
            while (true) {
                try (Socket socket = serverSocket.accept()) {
                    BufferedReader entrada = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                    PrintWriter salida = new PrintWriter(socket.getOutputStream(), true);

                    String saludoRecibido = entrada.readLine();

                    if (saludoRecibido != null && saludoRecibido.equalsIgnoreCase("Hola")) {

                        LocalDate hoy = LocalDate.now();
                        String diaHoy = traducirDia(hoy.getDayOfWeek().toString());

                        int posicionDia = 0;
                        for (int i = 0; i < diasSemana.length; i++) {
                            if (diasSemana[i].equals(diaHoy)) {
                                posicionDia = i + 1;
                                break;
                            }
                        }

                        String diaCita = diasSemana[(posicionDia + 2) % 7];
                        String calleCita = calles[(posicionDia + 2) % 7];

                        int horaCalculada = (posicionDia + 3) + 12;
                        String horaStr = horaCalculada + ":00";

                        String textoPlano = diaCita + " A LAS " + horaStr + " EN LA CALLE " + calleCita;
                        String criptograma = aplicarVigenere(textoPlano, diaHoy, true);

                        salida.println(diaHoy + "|" + criptograma);
                    }
                }
            }
        } catch (IOException e) { e.printStackTrace(); }
    }

    public static void cliente() {
        Scanner sc = new Scanner(System.in);
        System.out.println("--- CLIENTE ---");
        System.out.print("Escribe 'Hola' para contactar al servidor: ");
        String input = sc.nextLine();

        if (input.equalsIgnoreCase("Hola")) {
            try (Socket socket = new Socket("localhost", 5000)) {
                PrintWriter salida = new PrintWriter(socket.getOutputStream(), true);
                BufferedReader entrada = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                salida.println(input);

                String respuesta = entrada.readLine();
                if (respuesta != null) {
                    String[] partes = respuesta.split("\\|");
                    String clave = partes[0];
                    String criptograma = partes[1];

                    String descifrado = aplicarVigenere(criptograma, clave, false);

                    System.out.println("\n--- RESULTADO RECIBIDO ---");
                    System.out.println("MENSAJE CIFRADO:   " + criptograma);
                    System.out.println("--------------------------");
                    System.out.println("MENSAJE DESCIFRADO: " + descifrado);
                }
            } catch (IOException e) { e.printStackTrace(); }
        }
    }

    public static String aplicarVigenere(String texto, String clave, boolean cifrar) {
        StringBuilder resultado = new StringBuilder();
        int L = alfabeto.length();
        int j = 0;
        for (int i = 0; i < texto.length(); i++) {
            char c = texto.charAt(i);
            int Xi = alfabeto.indexOf(c);
            if (Xi == -1) { resultado.append(c); continue; }
            int Ki = alfabeto.indexOf(clave.charAt(j % clave.length()));

            int Ci = cifrar ? (Xi + Ki) % L : (Xi - Ki + L) % L;
            resultado.append(alfabeto.charAt(Ci));
            j++;
        }
        return resultado.toString();
    }

    private static String traducirDia(String diaIngles) {
        return switch (diaIngles) {
            case "MONDAY" -> "LUNES";
            case "TUESDAY" -> "MARTES";
            case "WEDNESDAY" -> "MIERCOLES";
            case "THURSDAY" -> "JUEVES";
            case "FRIDAY" -> "VIERNES";
            case "SATURDAY" -> "SABADO";
            case "SUNDAY" -> "DOMINGO";
            default -> "LUNES";
        };
    }
}