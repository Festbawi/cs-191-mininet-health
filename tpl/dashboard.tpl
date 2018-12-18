<!DOCTYPE HTML>
<html>
    <head>
        <title>Mininet Health Verifier</title>
        <link rel="stylesheet" href="/css/siimple.min.css">
    </head>

    <body>
        <div class="siimple-navbar siimple-navbar--large siimple-navbar--purple">
            <a class="siimple-navbar-title">Mininet Health Verifier</a>
            <div class="siimple-navbar-subtitle">Dashboard</div>
            <div class="siimple--float-right">
                <div class="siimple-btn siimple-btn--light" onClick="window.location.href=window.location.href">Refresh</div>
            </div>
        </div>
        
        <div class="siimple-content siimple-content--large">
            <div id="adj-modal" class="siimple-modal siimple-modal--medium" style="display:none;">
                <div class="siimple-modal-content">
                    <div class="siimple-modal-header">
                        <div class="siimple-modal-header-title">Node Link Adjacency</div>
                        <div id="adj-modal-close" class="siimple-modal-header-close"></div>
                    </div>
                    <div class="siimple-modal-body">
                        <div class="siimple-table">
                            <div class="siimple-table-header">
                                <div class="siimple-table-row">
                                        <div class="siimple-table-cell"></div>
                                %for node in adj['nodes']:
                                    <div class="siimple-table-cell">{{node}}</div>
                                %end
                                </div>
                            </div>
                            <div class="siimple-table-body">
                            %for i, adj_row in enumerate(adj['table']):
                                <div class="siimple-table-row">
                                    <div class="siimple-table-cell">{{adj['nodes'][i]}}</div>
                                    %for is_adjacent in adj_row:
                                        <div class="siimple-table-cell siimple--bg-{{'success' if is_adjacent else 'error siimple--color-white'}}">{{is_adjacent}}</div>
                                    %end
                                </div>
                            %end
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="siimple-h4">Network Details</div>
            <blockquote class="siimple-blockquote">
                %if not net:
                <span class="siimple-h6" style="margin-top: 10px !important;">No Mininet is supplied.</span>
                %else:
                    <span class="siimple-h6">Controller(s):</span>
                    %if not net.controllers:
                        &emsp;<span class="siimple--text-italic">None</span>
                    %else:
                        %for controller in net.controllers:
                            &emsp;{{controller.name}}
                        %end
                    %end
                    <span class="siimple-h6" style="margin-top: 10px !important;">Host(s):</span>
                    %if not net.hosts:
                        &emsp;<span class="siimple--text-italic">None</span>
                    %else:
                        %for host in net.hosts:
                            &emsp;{{host.name}}
                        %end
                    %end
                    <span class="siimple-h6" style="margin-top: 10px !important;">Switch(s):</span>
                    %if not net.switches:
                        &emsp;<span class="siimple--text-italic">None</span>
                    %else:
                        %for switch in net.switches:
                            &emsp;{{switch.name}}
                        %end
                    %end
                    <br/><span class="siimple-h6" style="display: inline-block !important; margin-top: 10px !important;">Link(s):</span>
                    &emsp;<div id="adj-modal-open" class="siimple-btn siimple-btn--purple siimple-btn--small">View adjacency matrix</div><br/>
                    %if not net.links:
                        &emsp;<span class="siimple--text-italic">None</span>
                    %else:
                        %for link in net.links:
                            &emsp;{{'%s-%s' % ( link.intf1.node.name, link.intf2.node.name )}}
                        %end
                    %end
                %end
            </blockquote>
            %if net is not None:
                <div id="verify-btn" class="siimple-btn siimple-btn--purple siimple--mb-4" align="center">Verify Health</div>
                <div id="result-div" style="display: none;">
                    <div class="siimple-h4">Diagnosis</div>
                    <pre id="result-pre" class="siimple-pre" style="resize: both; overflow: auto; height: 300px"></pre>
                </div>
            %end
        </div>

        <script src="/js/script.js"></script>
    </body>
</html>