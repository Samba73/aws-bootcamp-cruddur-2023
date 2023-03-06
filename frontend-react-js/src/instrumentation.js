import {WebTracerProvider} from "@opentelemetry/sdk-trace-web";
import {BatchSpanProcessor} from "@opentelemetry/sdk-trace-base";
//import {ZipkinExporter} from "@opentelemetry/exporter-zipkin";
import {W3CTraceContextPropagator} from "@opentelemetry/core";
import {registerInstrumentations} from "@opentelemetry/instrumentation";
import {SemanticResourceAttributes} from "@opentelemetry/semantic-conventions";
import {Resource} from "@opentelemetry/resources";
import {ZoneContextManager} from "@opentelemetry/context-zone";
import {FetchInstrumentation} from "@opentelemetry/instrumentation-fetch";
import { XMLHttpRequestInstrumentation } from '@opentelemetry/instrumentation-xml-http-request';
import {OTLPTraceExporter} from "@opentelemetry/exporter-trace-otlp-http";
import { DocumentLoadInstrumentation } from '@opentelemetry/instrumentation-document-load';

export const initInstrumentation = () => {
    const exporter = new OTLPTraceExporter({
        // optional - url default value is http://localhost:4318/v1/traces
        url: `${process.env.REACT_APP_OTEL_COLLECTOR_URL}/v1/traces`,
    });
    const resource = new Resource({
        [SemanticResourceAttributes.SERVICE_NAME]: "Cruddur",
    });

    const provider = new WebTracerProvider(resource);
    provider.addSpanProcessor(new BatchSpanProcessor(exporter));

    // Initialize the provider
    provider.register({
        propagator: new W3CTraceContextPropagator(),
        contextManager: new ZoneContextManager(),
    });

    // Registering instrumentations / plugins
    registerInstrumentations({
      instrumentations: [
        new XMLHttpRequestInstrumentation({
          propagateTraceHeaderCorsUrls: [
            new RegExp(`${process.env.REACT_APP_BACKEND_URL}`, 'g')
          ]
        }),
        new FetchInstrumentation({
          propagateTraceHeaderCorsUrls: [
            new RegExp(`${process.env.REACT_APP_BACKEND_URL}`, 'g')
          ]
        }),
        new DocumentLoadInstrumentation(),
      ],
    });
};