/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.pyropath.air.gui;

import edu.stanford.ejalbert.BrowserLauncher;
import edu.stanford.ejalbert.exception.BrowserLaunchingInitializingException;
import edu.stanford.ejalbert.exception.UnsupportedOperatingSystemException;
import java.awt.Desktop;
import javafx.application.Application;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

import java.io.IOException;
import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.UnknownHostException;
import java.util.logging.Level;
import java.util.logging.Logger;
import javafx.application.Platform;
import javafx.scene.control.Label;
import javafx.scene.layout.VBox;

import javax.jmdns.JmDNS;
import javax.jmdns.ServiceEvent;
import javax.jmdns.ServiceInfo;
import javax.jmdns.ServiceListener;

/**
 *
 * @author aretas-switch1
 */
public class AretasGatewayFinder extends Application {
    
    private final String mDnsType = "_http._tcp.local.";
    private String serviceUrl = "";
    Button btn;
    Button btnLaunch;
    Label txtLabel;
    private String lblTxt = "";
    
    @Override
    public void start(Stage primaryStage) {
        
        VBox vbButtons = new VBox();
        vbButtons.setSpacing(10);

        btn = new Button();
        btnLaunch = new Button();
        txtLabel = new Label();
        txtLabel.setWrapText(true);
        txtLabel.setText(lblTxt);
        
        btn.setText("Search for IoT Gateway");
        btnLaunch.setText("Launch Browser");
        btnLaunch.setDisable(true);
      
        btn.setOnAction(new btnHandler());
        btnLaunch.setOnAction(new btnLaunchHandler());
        
       
        vbButtons.getChildren().addAll(btn, btnLaunch, txtLabel);
        StackPane root = new StackPane();
        root.getChildren().add(vbButtons);
        
        Scene scene = new Scene(root, 300, 250);
        
        primaryStage.setTitle("Aretas Gateway Finder");
        primaryStage.setScene(scene);
        primaryStage.show();
    }
    
    private synchronized void appendLabelText(String txt){
        
        Platform.runLater(new Runnable(){
            

            @Override
            public void run() {
                lblTxt = lblTxt + txt;
                txtLabel.setText(lblTxt);
            }
        });
    
        
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        
        launch(args);
    }
    
    private class btnHandler implements EventHandler<ActionEvent>{
        
        @Override
        public void handle(ActionEvent event){
            
            try {
                
                // Create a JmDNS instance
                JmDNS jmdns = JmDNS.create(InetAddress.getLocalHost());

                // Add a service listener
                //jmdns.addServiceListener("_http._tcp.local.", new SampleListener());
                jmdns.addServiceListener(mDnsType, new SampleListener());

                
            } catch (UnknownHostException e) {
                System.out.println(e.getMessage());
            } catch (IOException e) {
                System.out.println(e.getMessage());
            }
        }
    }
    
     private class btnLaunchHandler implements EventHandler<ActionEvent>{
        
        @Override
        public void handle(ActionEvent event){
            System.out.println("Launching browser...");
            launchURL(serviceUrl);
        }
    }
    
    private class SampleListener implements ServiceListener {
        
        @Override
        public void serviceAdded(ServiceEvent event) {
            System.out.println("Service added: " + event.getInfo());
        }

        @Override
        public void serviceRemoved(ServiceEvent event) {
            System.out.println("Service removed: " + event.getInfo());
        }

        @Override
        public void serviceResolved(ServiceEvent event) {
            
            System.out.println("Service resolved: " + event.getInfo());
            
            ServiceInfo info = event.getInfo();
            
            System.out.println("SERVICE NAME:" + info.getName());
            
            appendLabelText("SVC NAME:" + info.getName() + "\n");
          
            if(info.getName().compareToIgnoreCase("aretasgw") == 0){
                Inet4Address inet4[] = info.getInet4Addresses();
                
                //try the first one?
                serviceUrl = "http://" + inet4[0].getHostAddress();
                //filter on the aretas gw service and get the address / url and then 
                //enable the browser launch button
                 btnLaunch.setDisable(false);
            }
    
        }
    }
    
    private static void launchURL2(String url){
        
        BrowserLauncher launcher;
        try {
            launcher = new BrowserLauncher();
            launcher.openURLinBrowser(url);
            
        } catch (BrowserLaunchingInitializingException ex) {
            Logger.getLogger(AretasGatewayFinder.class.getName()).log(Level.SEVERE, null, ex);
        } catch (UnsupportedOperatingSystemException ex) {
            Logger.getLogger(AretasGatewayFinder.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        
    }
    
    private static void launchURL(String url){
        
        if (Desktop.isDesktopSupported()) {
            
            try {
                //Windows
                Desktop.getDesktop().browse(new URI(url));
            } catch (IOException | URISyntaxException ex) {
                Logger.getLogger(AretasGatewayFinder.class.getName()).log(Level.SEVERE, null, ex);
            }
        } else {
            
            // Ubuntu
            Runtime runtime = Runtime.getRuntime();
            try {
                runtime.exec("/usr/bin/firefox -new-window " + url);
            } catch (IOException ex) {
                Logger.getLogger(AretasGatewayFinder.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
           
    }
}
