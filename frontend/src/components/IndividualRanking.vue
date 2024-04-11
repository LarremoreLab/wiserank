<template>
  <div>
    <svg class="svg simulation" :width="rankWidth" :height="rankHeight" transform="translate(0,0)">
        <g id="arcs">
        </g>
        <g id="items">
        </g>
    </svg>
  </div>
</template>

<script>
import * as d3 from 'd3';

export default {
  props: ['items', 'comparisons'],
  data: () =>({
    rankWidth: 200, //375,
    rankHeight: 300,
    compared: [],
    numNodes: 0,
    nodes: [],
    rankBounds: [-1, 1],
    nodeRadius: 5,
    nodeYs: {}
  }),
  async mounted() {
    this.buildRanking() 
  },
  methods: {
    computeY(rank, order){
      const y = (this.rankBounds[1] - rank) / (this.rankBounds[1] - this.rankBounds[0])
      return (y*(this.rankHeight - 2.3*this.nodeRadius*(this.compared.length) - 2)+
                (2.3*this.nodeRadius)*(.5 + order)
             ) + 1
    },
    addNode(item){
      const tx = this.rankWidth/2
      const ty = this.computeY(item[1], this.numNodes)
      this.nodeYs[item[0]] = ty
      this.nodes.push({'id':item[0], 'name':item[2], 'tx':tx, 'ty':ty}) // , 'x': tx, 'y': ty
      this.numNodes ++
    },
    parseItems(){
      for (let i = 0; i < this.items.length; i++) {
          if (this.compared.includes(this.items[i][0])){
              this.addNode(this.items[i])
          }
      } 
    },
    drawPath(){
      let radius = this.nodeRadius
      return " m -"+radius+", 0 a "+radius+","+radius+" 0 1,0 "+2*radius+",0 a "+radius+","+radius+" 0 1,0 -"+2*radius+",0"
    },
    initializeSim(){
        var that = this
        this.sliding = d3.forceSimulation()
        this.sliding.on("tick", function(){
                    d3.select('#items').selectAll('path')
                      .attr('transform', function(d) {
                          return "translate("+d.tx+','+d.ty+')'
                          })
                    d3.select('#arcs')
                        .selectAll("path")
                        .attr("d", function(d){
                            var wy = that.nodeYs[d[0]]
                            var ly = that.nodeYs[d[1]]
                            const side = ly - wy
                            const tx = that.rankWidth/2
                            const r = that.nodeRadius
                            var x0 = side > 0 ? tx + r/Math.sqrt(2): tx - r/Math.sqrt(2)
                            var x1 = side > 0 ? tx + r/Math.sqrt(2): tx - r/Math.sqrt(2)

                            var y0 = side > 0 ? wy + r/Math.sqrt(2) : wy - r/Math.sqrt(2)
                            var y1 = side > 0 ? ly - r/Math.sqrt(2) : ly + r/Math.sqrt(2)

                            return "M"+x0+
                                    ","+y0+
                                    "Q"+(that.rankWidth/2 + that.rankWidth*side/that.rankHeight)+","+(wy + side/3)+","+
                                    x1+","+y1
                        })
                  });
    },
    drawVisual(){
      var that = this

      d3.select('#arcs')
        .selectAll("path")
        .data(this.comparisons.filter(x => !x[2]), d => 'a'+d[0]+'b'+d[1])
        .join("path")
        .attr("id", function(d){return 'a'+d[0]+'b'+d[1]})
        .style("fill", "none")
        .style("stroke-width", ".5px")
        .style("stroke", "#9E9E9E")
        .style("opacity",.4)

      d3.select('#items')                                          
        .selectAll("path")
        .data(that.nodes, function(d){return d.id})
        .join("path")
        .attr("id",function(d){return d.id})
        .attr("d", function(){
            return that.drawPath()
        })
        .attr("transform", d => "translate("+d.tx+","+d.ty+")")
        .attr("r", function(){return that.nodeRadius})
        .style("fill", function(){return "black"})
        .style("fill-opacity", function(){return .45})
        .style("stroke", function(){return "black"})
        .style("stroke-width", function(){return .8})
        .style("stroke-opacity", function(){return .85})
        .on("mouseover", function() {that.$emit('hovered', {"name": this.__data__.name})})				
        .on("mouseout", function() {that.$emit('hovered', {"name":''})})

      this.sliding.nodes(this.nodes).alpha(1).restart()

    },
    buildRanking(){
      this.compared = [...new Set(this.comparisons.map(x => (x.slice(0,2))).flat())];

      // const targetRadius = this.rankHeight / 2 / 2 / this.compared.length
      // this.nodeRadius =  Math.max(1, Math.min(10, targetRadius))
      this.rankHeight = this.compared.length * this.nodeRadius * 4
      this.rankWidth = this.rankHeight / 2

      this.rankBounds = [this.items.slice(-1)[0][1],
                         this.items[0][1]]
      this.initializeSim()
      this.parseItems()
      this.drawVisual()
    }
  }
}
</script>
