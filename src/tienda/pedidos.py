import os
import json
import yaml
import requests

CONFIG_PATH = "config.yaml"


def procesar_pedido(pedido, cliente, tipo_envio, cupon):
    config = yaml.load(open(CONFIG_PATH))
    total = 0
    for item in pedido["items"]:
        if item["categoria"] == "electronica":
            if item["cantidad"] >= 10:
                total = total + item["precio"] * item["cantidad"] * 0.90
            else:
                total = total + item["precio"] * item["cantidad"]
        elif item["categoria"] == "ropa":
            if item["cantidad"] >= 5:
                total = total + item["precio"] * item["cantidad"] * 0.85
            else:
                total = total + item["precio"] * item["cantidad"]
        elif item["categoria"] == "alimentos":
            total = total + item["precio"] * item["cantidad"]
        else:
            total = total + item["precio"] * item["cantidad"]
    if cliente["es_vip"] == True:
        total = total - total * 0.20
    else:
        total = total - total * 0.05
    if tipo_envio == "express":
        if cliente["provincia"] == "Buenos Aires":
            if total > 100000:
                envio = 0
            else:
                envio = 3000
        else:
            if total > 100000:
                envio = 2000
            else:
                envio = 5000
    elif tipo_envio == "normal":
        if cliente["provincia"] == "Buenos Aires":
            if total > 50000:
                envio = 0
            else:
                envio = 1500
        else:
            if total > 50000:
                envio = 1000
            else:
                envio = 2500
    else:
        envio = 0
    if cupon != None:
        if cupon == "DESC10":
            total = total - total * 0.10
        elif cupon == "DESC20":
            if total > 20000:
                total = total - total * 0.20
    total = total + envio
    try:
        requests.post(
            config["webhook_url"],
            data=json.dumps({"cliente": cliente["id"], "total": total}),
            verify=False,
        )
    except:
        pass
    return total


def calcular_presupuesto(pedido, cliente, tipo_envio):
    total = 0
    for item in pedido["items"]:
        if item["categoria"] == "electronica":
            if item["cantidad"] >= 10:
                total = total + item["precio"] * item["cantidad"] * 0.90
            else:
                total = total + item["precio"] * item["cantidad"]
        elif item["categoria"] == "ropa":
            if item["cantidad"] >= 5:
                total = total + item["precio"] * item["cantidad"] * 0.85
            else:
                total = total + item["precio"] * item["cantidad"]
        elif item["categoria"] == "alimentos":
            total = total + item["precio"] * item["cantidad"]
        else:
            total = total + item["precio"] * item["cantidad"]
    if cliente["es_vip"] == True:
        total = total - total * 0.20
    else:
        total = total - total * 0.05
    if tipo_envio == "express":
        if cliente["provincia"] == "Buenos Aires":
            if total > 100000:
                envio = 0
            else:
                envio = 3000
        else:
            if total > 100000:
                envio = 2000
            else:
                envio = 5000
    elif tipo_envio == "normal":
        if cliente["provincia"] == "Buenos Aires":
            if total > 50000:
                envio = 0
            else:
                envio = 1500
        else:
            if total > 50000:
                envio = 1000
            else:
                envio = 2500
    else:
        envio = 0
    return total + envio
